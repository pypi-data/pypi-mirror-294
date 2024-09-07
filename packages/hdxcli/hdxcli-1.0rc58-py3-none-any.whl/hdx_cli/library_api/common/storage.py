from typing import Union, Tuple, Optional

from hdx_cli.library_api.common.context import ProfileUserContext
from hdx_cli.library_api.common.exceptions import HdxCliException
from hdx_cli.library_api.common.generic_resource import access_resource_detailed


def is_same_bucket(settings_source: dict, settings_target: dict) -> bool:
    result = False
    if (
            settings_source.get('bucket_name') == settings_target.get('bucket_name') and
            settings_source.get('bucket_path') == settings_target.get('bucket_path') and
            settings_source.get('region') == settings_target.get('region') and
            settings_source.get('cloud') == settings_target.get('cloud')
    ):
        result = True
    return result


def look_for_same_bucket(settings: dict, storages: list[dict]) -> Union[str, None]:
    for storage in storages:
        if is_same_bucket(settings, storage.get('settings')):
            return storage.get('uuid')
    return None


def get_equivalent_storages(source_storages: list[dict],
                            target_storages: list[dict]
                            ) -> dict[str, str]:
    result_dict = {}
    for source_storage in source_storages:
        source_storage_settings = source_storage.get('settings')
        target_storage_uuid = look_for_same_bucket(source_storage_settings, target_storages)
        if target_storage_uuid:
            result_dict[source_storage.get('uuid')] = target_storage_uuid

            # Default source storage added to map it when null storage_id values
            # exist in catalog records
            if source_storage_settings.get('is_default'):
                result_dict['default'] = target_storage_uuid
    return result_dict


def matching_tables_storage_mapping(source_profile: ProfileUserContext,
                                    target_profile: ProfileUserContext,
                                    target_storages: list
                                    ) -> dict[str, str]:
    source_table, _ = access_resource_detailed(
        source_profile,
        [
            ('projects', source_profile.projectname),
            ('tables', source_profile.tablename)
        ]
    )
    target_table, _ = access_resource_detailed(
        target_profile,
        [
            ('projects', target_profile.projectname),
            ('tables', target_profile.tablename)
        ]
    )

    matching_uuids = {}
    source_storage_map = source_table.get('settings', {}).get('storage_map', {})
    target_storage_map = target_table.get('settings', {}).get('storage_map', {})

    source_default_storage_id = source_storage_map.get('default_storage_id')
    target_default_storage_id = target_storage_map.get('default_storage_id')

    if source_default_storage_id and target_default_storage_id:
        matching_uuids[source_default_storage_id] = target_default_storage_id
    elif target_default_storage_id:
        matching_uuids['default'] = target_default_storage_id
    else:
        matching_uuids['default'], _= get_storage_default(target_storages)

    source_column_mapping = source_storage_map.get('column_value_mapping')
    target_column_mapping = target_storage_map.get('column_value_mapping')

    if (
            not source_column_mapping and not target_column_mapping or
            source_column_mapping and not target_column_mapping
    ):
        return matching_uuids
    elif target_column_mapping and not source_column_mapping:
        raise HdxCliException(
            "The target table has 'column_value_mapping' set, but the source table does not."
        )

    if len(source_column_mapping) != len(target_column_mapping):
        raise HdxCliException(
            "Tables do not have the same number of elements in 'column_value_mapping'."
        )

    for uuid1, value1 in source_column_mapping.items():
        for uuid2, value2 in target_column_mapping.items():
            if value1 == value2:
                matching_uuids[uuid1] = uuid2

    # Why + 1? Because the default storage (default_storage_id) is also part of the mapping
    if len(matching_uuids) != len(target_column_mapping) + 1:
        raise HdxCliException(
            "Not all elements in 'column_value_mapping' have "
            'a matching value between the tables.'
        )
    return matching_uuids


def get_storage_by_id(storages: list[dict], storage_id: str) -> Tuple[str, Optional[dict]]:
    for storage in storages:
        if storage.get('uuid') == storage_id:
            return storage_id, storage.get('settings')
    return storage_id, None


def get_storage_default(storages: list[dict]) -> Tuple[Optional[str], Optional[dict]]:
    for storage in storages:
        if storage.get('settings', {}).get('is_default'):
            return storage.get('uuid'), storage.get('settings')
    return None, None
