import copy
import json
from urllib.parse import urlparse

from .helpers import MigrationData, confirm_action
from hdx_cli.cli_interface.common.undecorated_click_commands import basic_create_with_body_from_string
from hdx_cli.library_api.common.exceptions import HttpException, ResourceNotFoundException, HdxCliException
from hdx_cli.library_api.common.generic_resource import access_resource_detailed
from hdx_cli.library_api.common.logging import get_logger
from hdx_cli.library_api.common.storage import get_equivalent_storages
from hdx_cli.library_api.common.context import ProfileUserContext

logger = get_logger()


def creating_resources(target_profile: ProfileUserContext,
                       target_data: MigrationData,
                       source_data: MigrationData,
                       reuse_partitions: bool = False
                       ) -> None:
    logger.info(f'{" Resources ":=^50}')
    logger.info(f"{f'Creating resources in {target_profile.hostname[:27]}':<50}")

    # PROJECT
    logger.info(f"{f'  Project: {target_profile.projectname[:31]}':<42} -> [!n]")
    _, target_projects_url = access_resource_detailed(target_profile, [('projects', None)])
    target_projects_path = urlparse(f'{target_projects_url}').path

    source_project_body = copy.deepcopy(source_data.project)
    try:
        if not reuse_partitions:
            del source_project_body['uuid']
        basic_create_with_body_from_string(
            target_profile,
            target_projects_path,
            target_profile.projectname,
            json.dumps(source_project_body)
        )
        logger.info('Done')
    except HttpException as exc:
        if exc.error_code != 400 or 'already exists' not in str(exc.message):
            raise exc
        logger.info('Exists, skipping')

    target_data.project, target_project_url = access_resource_detailed(
        target_profile,
        [
            ('projects', target_profile.projectname)
        ]
    )
    if reuse_partitions and source_project_body.get('uuid') != target_data.project.get('uuid'):
        raise HdxCliException('The source and target resources must have the same UUID.')

    # TABLE
    logger.info(f"{f'  Table: {target_profile.tablename[:33]}':<42} -> [!n]")
    target_tables_path = urlparse(f'{target_project_url}tables/').path
    table_body = copy.deepcopy(source_data.table)
    if not reuse_partitions:
        del table_body['uuid']
    basic_create_with_body_from_string(
        target_profile,
        target_tables_path,
        target_profile.tablename,
        json.dumps(table_body)
    )
    logger.info('Done')

    target_data.table, target_table_url = access_resource_detailed(
        target_profile,
        [
            ('projects', target_profile.projectname),
            ('tables', target_profile.tablename)
        ]
    )

    # TRANSFORMS
    # If table type is summary, then there are no transforms to create
    # TODO: workaround to avoid creating transforms in summary tables
    if table_body.get('type') == 'summary':
        return

    logger.info(f"{f'  Transforms':<42} -> [!n]")
    target_transforms_path = urlparse(f'{target_table_url}transforms/').path
    for transform in source_data.transforms:
        del transform['uuid']
        transform_name = transform.get('name')
        basic_create_with_body_from_string(
            target_profile,
            target_transforms_path,
            transform_name,
            json.dumps(transform)
        )
    logger.info('Done')
    logger.info('')


def get_resources(profile: ProfileUserContext,
                  data: MigrationData,
                  only_storages: bool = False
                  ) -> None:
    logger.info(f"{f'Getting resources from {profile.hostname[:27]}':<50}")

    if not only_storages:
        logger.info(f'{f"  Project: {profile.projectname[:31]}":<42} -> [!n]')
        data.project, _ = access_resource_detailed(profile, [('projects', profile.projectname)])
        if not data.project:
            raise ResourceNotFoundException(f"The project '{profile.projectname}' was not found.")
        logger.info('Done')

        logger.info(f"{f'  Table: {profile.tablename[:33]}':<42} -> [!n]")
        data.table, _ = access_resource_detailed(
            profile,
            [
                ('projects', profile.projectname),
                ('tables', profile.tablename)
            ]
        )
        if not data.table:
            raise ResourceNotFoundException(f"The table '{profile.tablename}' was not found.")
        logger.info('Done')

        logger.info(f"{'  Transforms':<42} -> [!n]")
        data.transforms, _ = access_resource_detailed(
            profile,
            [
                ('projects', profile.projectname),
                ('tables', profile.tablename),
                ('transforms', None)
            ]
        )
        if not data.transforms:
            raise ResourceNotFoundException(
                f"Transforms in the table '{profile.tablename}' were not found."
            )
        logger.info('Done')

    # Then, storages
    logger.info(f"{'  Storages':<42} -> [!n]")
    data.storages, _ = access_resource_detailed(profile, [('storages', None)])
    logger.info('Done')


def update_multi_bucket_settings(source_data: MigrationData,
                                 target_storages: list[dict],
                                 reuse_partitions: bool
                                 ) -> None:
    """
    Update multi-bucket settings for the target table. If reuse_partitions is True,
    then the function will update the default_storage_id and column_value_mapping
    with the equivalent storage (from the source to the target storages).
    Whether reuse_partitions is False, the function will prompt the user to provide
    the new default_storage_id and column_value_mapping.
    """
    if not reuse_partitions:
        interactive_update_multi_bucket_settings(source_data, target_storages)
        return

    storage_equivalences = get_equivalent_storages(source_data.storages, target_storages)
    table_body = source_data.table
    storage_map = table_body.get('settings').get('storage_map')
    default_storage_id = storage_map.get('default_storage_id')
    if not (new_default_storage_id := storage_equivalences.get(default_storage_id)):
        raise HdxCliException(
            f"Storage ID '{default_storage_id}' not found in the target storages."
        )

    storage_map['default_storage_id'] = new_default_storage_id

    if mapping := storage_map.get('column_value_mapping'):
        new_mapping = {}
        for storage, values in mapping.items():
            if not (new_storage := storage_equivalences.get(default_storage_id)):
                raise HdxCliException(
                    f"Storage ID '{default_storage_id}' not found in the target storages."
                )
            new_mapping[new_storage] = values
        storage_map['column_value_mapping'] = new_mapping


def interactive_update_multi_bucket_settings(source_data: MigrationData,
                                            target_storages: list[dict]
                                            ) -> None:
    logger.info('')
    logger.info('')
    table_body = source_data.table
    storage_map = table_body.get('settings').get('storage_map')

    logger.info(f'{" Multi-bucket settings ":-^50}')
    assert isinstance(storage_map, dict)
    for key, value in storage_map.items():
        logger.info(f'{key}: {value}')

    logger.info('')
    logger.info('If the current multi-bucket settings need to be retained,')
    logger.info('it will be necessary to provide the storage UUIDs from the target cluster.')
    if not confirm_action(prompt='Do you want to retain this multi-bucket settings?'):
        logger.info(f'{"  ":-^40}')
        logger.info(f"{'  Removing multi-bucket settings':<42} -> [!n]")
        del table_body['settings']['storage_map']
        return

    logger.info('')
    logger.info("Please, provide 'default_storage_id': [!i]")
    new_default_storage_id = input().lower()
    valid_storage_id(new_default_storage_id, target_storages)
    storage_map['default_storage_id'] = new_default_storage_id

    default_column_value_mapping = storage_map.get('column_value_mapping')
    if default_column_value_mapping:
        new_column_value_mapping = {}
        assert isinstance(default_column_value_mapping, dict)
        logger.info('Column value mapping')
        for _, value in default_column_value_mapping.items():
            logger.info(f'  Values: {value}')
            logger.info('  Specify storage UUID for these values: [!i]')
            new_storage_id = input().lower()
            valid_storage_id(new_storage_id, target_storages)
            new_column_value_mapping[new_storage_id] = value
        storage_map['column_value_mapping'] = new_column_value_mapping

    logger.info(f'{"  ":-^50}')
    logger.info(f"{'  Updating multi-bucket settings':<42} -> [!n]")


def set_default_bucket(source_data: MigrationData, target_storages: list[dict]) -> None:
    logger.info('')
    logger.info('')
    table_body = source_data.table

    logger.info(f'{" Default Storage Settings ":-^50}')
    logger.info('No multi-bucket settings were found for the table.')
    logger.info('If no storage UUID is specified, ')
    logger.info('the target cluster’s default storage will be used.')
    logger.info('')

    if confirm_action(prompt='Do you want to specify a default storage?'):
        logger.info('Please, provide the default storage UUID: [!i]')
        default_storage_id = input().lower()
        valid_storage_id(default_storage_id, target_storages)
        table_settings = table_body.get('settings')
        table_settings['storage_map'] = {'default_storage_id': default_storage_id}

    logger.info(f'{"  ":-^40}')
    logger.info(f"{'  Updating default storage settings':<42} -> [!n]")
    return


def valid_storage_id(storage_id: str, storages: list[dict]) -> None:
    if not storage_id or storage_id not in [storage.get('uuid') for storage in storages]:
        raise HdxCliException(
            f"Storage ID '{storage_id}' not found in the target storages."
        )
