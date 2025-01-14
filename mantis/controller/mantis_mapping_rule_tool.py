import json

from common_tools.tools import create_current_format_time, op11_redis_client
from mantis.models import mantis_db
from mantis.models.mantis_config import MantisMappingRule


def mantis_create_mapping_rule_tool(request_params):
    current_time = create_current_format_time()
    sub_func_id2func_id = json.loads(op11_redis_client.get('field_id2value')).get('sub_func_id2func_id')
    mcm = MantisMappingRule(
        cluster_id=request_params.get('cluster'),
        project=request_params.get('project'),
        mapping_name=request_params.get('mapping_name'),
        mapping_rule=generate_mantis_mapping_rule(request_params, sub_func_id2func_id),
        create_time=current_time,
        update_time=current_time,
    )
    mantis_db.session.add(mcm)
    mantis_db.session.commit()


def generate_mantis_mapping_rule(request_params, sub_func_id2func_id):
    sub_function_list = request_params.get('sub_function')
    function_list = list({int(sub_func_id2func_id.get(str(i))) for i in sub_function_list})
    return {
        'function': sorted(function_list),
        'sub_function': sub_function_list,
        'fuLi_value': request_params.get('fuLi_id'),
        'category': request_params.get('category'),
        'level': request_params.get('level'),
        'cluster': [request_params.get('cluster')],
        'available_platform': request_params.get('available_platform'),
        'available_carline': request_params.get('available_carline'),
        'available_variant': request_params.get('available_variant'),
        'available_market': request_params.get('available_market'),
        'available_language': request_params.get('available_language'),
        'available_environment': request_params.get('available_environment'),
        'test_platform': request_params.get('test_platform'),
        'test_carline': request_params.get('test_carline'),
        'test_variant': request_params.get('test_variant'),
        'test_market': request_params.get('test_market'),
        'test_language': request_params.get('test_language'),
        'test_environment': request_params.get('test_environment'),
        'test_result': request_params.get('test_result'),
        'tb_type': request_params.get('tb_type')
    }


def mantis_edit_mapping_rule_tool(request_params):
    sub_func_id2func_id = json.loads(op11_redis_client.get('field_id2value')).get('sub_func_id2func_id')
    MantisMappingRule.query.filter(MantisMappingRule.id == request_params.get('id')).update({
        'mapping_name': request_params.get('mapping_name'),
        'project': request_params.get('project'),
        'cluster_id': request_params.get('cluster'),
        'mapping_rule': generate_mantis_mapping_rule(request_params, sub_func_id2func_id),
        'update_time': create_current_format_time()
    })
    mantis_db.session.commit()


def mantis_delete_mapping_rule_tool(request_params):
    MantisMappingRule.query.filter(MantisMappingRule.id == request_params.get('id')).delete()
    mantis_db.session.commit()


def mantis_get_mapping_rule_tool(request_params):
    page_size = request_params.get('page_size')
    page_num = request_params.get('page_num')
    project = request_params.get('project')
    filter_list = []
    if project:
        filter_list.append(MantisMappingRule.project_id == project)
    mcm = MantisMappingRule.query.filter(
        *filter_list
    ).order_by(
        MantisMappingRule.create_time.desc()
    ).offset((int(page_num) - 1) * page_size).limit(int(page_size)).all()
    mapping_rule_list = list(map(generate_mapping_rule, mcm))
    return mapping_rule_list


def generate_mapping_rule(mapping_rule):
    return {
        'id': mapping_rule.id,
        'mapping_name': mapping_rule.mapping_name,
        'mapping_rule': mapping_rule.mapping_rule,
        'project': mapping_rule.project,
        'cluster': mapping_rule.cluster_id,
        'function': len(mapping_rule.mapping_rule.get('function')) if
        mapping_rule.mapping_rule.get('function') else 0,
        'sub_function': len(mapping_rule.mapping_rule.get('sub_function')) if
        mapping_rule.mapping_rule.get('sub_function') else 0,
        'create_time': str(mapping_rule.create_time),
        'update_time': str(mapping_rule.update_time)
    }


def mantis_clone_mapping_rule_tool(request_params):
    mcm = MantisMappingRule.query.filter(MantisMappingRule.id == request_params.get('id')).first()
    current_time = create_current_format_time()
    mapping_rule = mcm.mapping_rule
    mapping_rule['cluster'] = [request_params.get('cluster')]
    mcm = MantisMappingRule(
        mapping_name=request_params.get('mapping_name'),
        project=request_params.get('project'),
        cluster_id=request_params.get('cluster'),
        mapping_rule=mapping_rule,
        create_time=current_time,
        update_time=current_time,
    )
    mantis_db.session.add(mcm)
    mantis_db.session.commit()


def mantis_check_mapping_name_tool(request_params):
    mcm = MantisMappingRule.query.filter(
        MantisMappingRule.mapping_name == request_params.get('mapping_name')
    ).first()
    if mcm:
        return False
    else:
        return True
