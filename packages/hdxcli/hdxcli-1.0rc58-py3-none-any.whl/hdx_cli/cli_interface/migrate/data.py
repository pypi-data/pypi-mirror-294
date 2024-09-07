import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

from .helpers import (
    print_summary,
    validate_files_amount,
    confirm_action,
    MigrationData,
    show_progress_bar,
    update_catalog_and_upload, upload_catalog
)
from .recovery import recovery_process
from .workers import CountingQueue, ReaderWorker, WriterWorker
from .catalog_operations import Catalog
from hdx_cli.library_api.common.context import ProfileUserContext
from hdx_cli.library_api.common.provider import get_provider
from hdx_cli.library_api.common.logging import get_logger
from hdx_cli.library_api.common.storage import matching_tables_storage_mapping

logger = get_logger()


def show_and_confirm_data_migration(catalog: Catalog, migrated_file_list: list) -> bool:
    """
    Displays a summary of the migration process,
    validates that the number of files to migrate is greater than 0,
    and asks for user confirmation to start the migration process.
    """
    total_rows, total_files, total_size = catalog.get_summary_information()
    migrated_files_count = len(migrated_file_list)
    print_summary(total_rows, total_files, total_size, migrated_files_count)
    return validate_files_amount(total_files, migrated_files_count) and confirm_action()


def migrate_data(target_profile: ProfileUserContext,
                 target_data: MigrationData,
                 source_profile: ProfileUserContext,
                 source_storages: list[dict],
                 catalog: Catalog,
                 workers_amount: int,
                 recovery: bool = False,
                 reuse_partitions: bool = False
                 ) -> None:
    logger.info(f'{" Data ":=^50}')

    if reuse_partitions:
        upload_catalog(target_profile, catalog)
        logger.info('')
        return

    storage_mapping = matching_tables_storage_mapping(
        source_profile,
        target_profile,
        target_data.storages
    )
    partition_paths_by_storage = catalog.get_partition_files_by_storage()
    partitions_size = catalog.get_total_size()

    # Migrating partitions
    migrated_files_queue = Queue()
    exceptions = Queue()

    workers_list = []
    writer_queues_list = []
    providers = {}
    files_count = 0
    migrated_file_list = []

    # Recovery point if exist
    if recovery:
        target_root_path = f'db/hdx/{target_data.get_project_id()}/{target_data.get_table_id()}'
        target_provider = get_provider(providers, target_data.storages)

        logger.info(f"{'Looking migrated files':<42} -> [!n]")
        migrated_file_list = target_provider.list_files_in_path(path=target_root_path)
        logger.info('Done')

    for source_storage_id, files_to_migrate in partition_paths_by_storage.items():
        # Get source and target providers
        target_storage_id = (
                storage_mapping.get(source_storage_id) or
                storage_mapping.get('default')
        )
        try:
            source_provider = get_provider(providers, source_storages, storage_id=source_storage_id)
            target_provider = get_provider(providers, target_data.storages, storage_id=target_storage_id)
        except Exception as exc:
            exceptions.put(exc)
            raise

        # Total amount of files to migrate
        files_count += len(files_to_migrate)

        # Are there files already migrated?
        if migrated_file_list:
            files_to_migrate = recovery_process(
                files_to_migrate,
                migrated_file_list,
                migrated_files_queue
            )

        reader_queue = CountingQueue(files_to_migrate)
        writer_queue = Queue()
        writer_queues_list.append(writer_queue)

        for _ in range(workers_amount):
            workers_list.append(
                ReaderWorker(
                    reader_queue,
                    writer_queue,
                    exceptions,
                    source_provider,
                    workers_amount,
                    target_data.get_project_id(),
                    target_data.get_table_id()
                )
            )
            workers_list.append(
                WriterWorker(
                    writer_queue,
                    migrated_files_queue,
                    exceptions,
                    target_provider
                )
            )

    # Before start the migration, show and ask for confirmation
    if not show_and_confirm_data_migration(catalog, migrated_file_list):
        logger.info(f'{" Migration Process Finished ":=^50}')
        logger.info('')
        sys.exit(0)

    # Start all workers once confirmed by the user
    with ThreadPoolExecutor(max_workers=workers_amount * 2) as executor:
        future_to_worker = {executor.submit(worker.start): worker for worker in workers_list}

        # Show progress bar while workers are running
        show_progress_bar(partitions_size, migrated_files_queue, exceptions)

        # Signal writers to stop by putting 'None' in the queue
        for writer_queue_item in writer_queues_list:
            for _ in range(workers_amount):
                writer_queue_item.put(None)

        # Wait for all workers to complete
        for future in as_completed(future_to_worker):
            try:
                future.result()
            except Exception as exc:
                exceptions.put(exc)

    if exceptions.qsize() != 0:
        exception = exceptions.get()
        raise exception

    update_catalog_and_upload(target_profile, catalog, target_data, storage_mapping)
    logger.info('')
