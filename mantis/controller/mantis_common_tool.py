import json

from common_tools.tools import create_current_format_time, op11_redis_client
from mantis.mantis_caches import mantis_update_sw_cache
from mantis.mantis_status import mantis_project, field_display_order, milestone_status, cycle_status, free_test_status, \
    label_mapping, mantis_project_to_cluster
from mantis.models import mantis_db
from mantis.models.case import SWMap


def get_common_info_tool():
    field_mapping = json.loads(op11_redis_client.get('field_id2value'))
    common_info = {
        'mantis_project': mantis_project,
        'mantis_project_to_cluster': mantis_project_to_cluster,
        'category': generate_field_dict(field_mapping.get('category')),
        'level': generate_field_dict(field_mapping.get('level')),
        'mantis_cluster': generate_field_dict(field_mapping.get('cluster')),
        'available_platform': generate_field_dict(field_mapping.get('available_platform')),
        'available_carline': generate_field_dict(field_mapping.get('available_carline')),
        'available_variant': generate_field_dict(field_mapping.get('available_variant')),
        'available_market': generate_field_dict(field_mapping.get('available_market')),
        'available_language': generate_field_dict(field_mapping.get('available_language')),
        'available_environment': generate_field_dict(field_mapping.get('available_environment')),
        'test_platform': generate_field_dict(field_mapping.get('test_platform')),
        'test_carline': generate_field_dict(field_mapping.get('test_carline')),
        'test_market': generate_field_dict(field_mapping.get('test_market')),
        'test_variant': generate_field_dict(field_mapping.get('test_variant')),
        'test_language': generate_field_dict(field_mapping.get('test_language')),
        'test_environment': generate_field_dict(field_mapping.get('test_environment')),
        'mantis_function': generate_field_dict(field_mapping.get('function')),
        'mantis_sub_function': generate_field_dict(field_mapping.get('sub_function')),
        'mantis_result': generate_field_dict(field_mapping.get('test_result')),
        'mantis_tb_type': generate_field_dict(field_mapping.get('tb_type')),
        'mantis_fuLi': json.loads(op11_redis_client.get('fuLi_group')),
        'field_display_order': field_display_order,
        'milestone_status': milestone_status,
        'cycle_status': cycle_status,
        'free_test_status': free_test_status,
        'label_mapping': label_mapping,
    }
    del field_mapping['fuLi_value']
    del field_mapping['function']
    del field_mapping['sub_function']
    del field_mapping['sub_func_id2func_id']
    common_info['field_mapping'] = field_mapping
    common_info['cluster'] = list(common_info.get('mantis_cluster').keys())
    return common_info


def generate_field_dict(field_mapping):
    return {int(key): value for key, value in field_mapping.items()}


def sw_map_tool(request_params):
    current_map = SWMap.query.filter(
        SWMap.sw_alpha == request_params.get('sw_alpha').strip(),
        SWMap.delete_flag == 0,
    ).first()
    current_time = create_current_format_time()
    if not current_map and request_params.get('delete_flag') == 0:
        sw_map = SWMap(
            sw_alpha=request_params.get('sw_alpha').strip(),
            sw_num=request_params.get('sw_num'),
            create_time=current_time,
            update_time=current_time,
            delete_flag=0
        )
        mantis_db.session.add(sw_map)
    elif current_map and request_params.get('delete_flag') == 1:
        current_map.delete_flag = request_params.get('delete_flag')
    elif current_map and request_params.get('delete_flag') == 0:
        current_map.sw_num = request_params.get('sw_num')
        current_map.update_time = current_time
    mantis_db.session.commit()
    mantis_update_sw_cache()
