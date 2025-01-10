# -*- coding: utf-8 -*-
import json

from common_tools.tools import op11_redis_client
from mantis.mantis_caches import mantis_update_field_mapping_rule
from mantis.models import mantis_db
from mantis.models.case import TestCase
from mantis.models.functions import SubFunction, Group, Functions, MantisCaseField, MantisFuLiGroup, MantisFuLi
from mantis.models.mantis_config import MantisMappingRule


def query_functions():
    func_dict = {}
    group_info = json.loads(op11_redis_client.get('group'))
    for key, value in group_info.items():
        func_dict[key] = {
            'function': {},
            'group_id': int(key),
            'group_name': value
        }
    functions = mantis_db.session.query(Functions).all()
    for function in functions:
        func_dict[str(function.test_group)]['function'][str(function.id)] = {
            'function_id': function.id,
            'function_name': function.function,
            'sub_function': {}
        }
    sub_functions = mantis_db.session.query(SubFunction).all()
    for sub_function in sub_functions:
        func_dict[
            str(sub_function.test_group)
        ]['function'][str(sub_function.function)]['sub_function'][str(sub_function.id)] = {
            'sub_function_id': sub_function.id,
            'sub_function_name': sub_function.sub_function,
        }
    return func_dict


def mantis_create_functions_tool(request_params):
    field = request_params.get('field')
    model_dict = {
        'group': Group,
        'function': Functions,
        'sub_function': SubFunction,
        'fuLi_group': MantisFuLiGroup,
        'fuLi': MantisFuLi,
    }
    check_field, param_field = generate_check_field(field)
    if mantis_check_function_exists_tool(
        model_dict,
        field,
        check_field,
        request_params.get(param_field)
    ):
        return False, 10017
    field_dict = {
        'group': Group(
            group_name=request_params.get('group_name')
        ),
        'function': Functions(
            test_group=request_params.get('mantis_group_id'),
            function=request_params.get('function_name')
        ),
        'sub_function': SubFunction(
            test_group=request_params.get('mantis_group_id'),
            function=request_params.get('function_id'),
            sub_function=request_params.get('sub_function_name')
        ),
        'fuLi_group': MantisFuLiGroup(
            fuLi_group_name=request_params.get('fuLi_group_name')
        ),
        'fuLi': MantisFuLi(
            fuLi_id=request_params.get('fuLi_id'),
            fuLi_group_id=request_params.get('fuLi_group_id'),
            fuLi_desc=request_params.get('fuLi_desc'),
            delete_flag=1
        )
    }

    mantis_model = field_dict.get(field)
    mantis_db.session.add(mantis_model)
    mantis_db.session.flush()
    new_id = mantis_model.id
    mantis_db.session.commit()
    mantis_update_field_mapping_rule()
    return True, new_id


def mantis_edit_functions_tool(request_params):
    field = request_params.get('field')
    model_dict = {
        'group': Group,
        'function': Functions,
        'sub_function': SubFunction,
        'fuLi_group': MantisFuLiGroup,
        'fuLi': MantisFuLi,
    }
    update_model = {
        'group': {
            'group_name': request_params.get('group_name')
        },
        'function': {
            'test_group': request_params.get('mantis_group_id'),
            'function': request_params.get('function_name')
        },
        'sub_function': {
            'test_group': request_params.get('mantis_group_id'),
            'function': request_params.get('function_id'),
            'sub_function': request_params.get('sub_function_name')
        },
        'fuLi_group': {
            'fuLi_group_name': request_params.get('fuLi_group_name')
        },
        'fuLi': {
            'fuLi_id': request_params.get('fuLi_id'),
            'fuLi_group_id': request_params.get('fuLi_group_id'),
            'fuLi_desc': request_params.get('fuLi_desc')
        }
    }
    model_dict.get(field).query.filter(
        model_dict.get(field).id == request_params.get('id')
    ).update(update_model.get(field))
    mantis_db.session.commit()
    mantis_update_field_mapping_rule()


def mantis_delete_functions_tool(request_params):
    if mantis_check_function_used_tool(request_params.get('field'), request_params.get('id')):
        return 10018

    def _cascade_clear_sub_functions(_field):
        mode_dict = {
            'group': SubFunction.test_group,
            'function': SubFunction.function,
        }
        sub_funcs = SubFunction.query.filter(mode_dict.get(_field) == request_params.get('id')).all()
        sub_funcs_list = [sub_func.id for sub_func in sub_funcs]
        map(lambda sub_func_id: mantis_clear_mapping_rule('sub_function', sub_func_id), sub_funcs_list)
        SubFunction.query.filter(mode_dict.get(_field) == request_params.get('id')).delete()

    def _cascade_clear_functions():
        sub_funcs = SubFunction.query.filter(Functions.test_group == request_params.get('id')).all()
        sub_funcs_list = [sub_func.id for sub_func in sub_funcs]
        map(lambda sub_func_id: mantis_clear_mapping_rule('function', sub_func_id), sub_funcs_list)
        SubFunction.query.filter(Functions.test_group == request_params.get('id')).delete()

    def _cascade_clear_fuli():
        fu_lis = MantisFuLi.query.filter(MantisFuLi.fuLi_group_id == request_params.get('id')).all()
        fu_lis_list = [fuLi.id for fuLi in fu_lis]
        map(lambda fu_lis_id: mantis_clear_mapping_rule('fuLi_value', fu_lis_id), fu_lis_list)
        MantisFuLi.query.filter(MantisFuLi.fuLi_group_id == request_params.get('id')).update({'delete_flag': 2})

    field = request_params.get('field')
    if field == 'group':
        Group.query.filter(Group.id == request_params.get('id')).delete()
        _cascade_clear_functions()
        _cascade_clear_sub_functions(field)
    elif field == 'function':
        Functions.query.filter(Functions.id == request_params.get('id')).delete()
        mantis_clear_mapping_rule(field, request_params.get('id'))
        _cascade_clear_sub_functions(field)
    elif field == 'sub_function':
        SubFunction.query.filter(SubFunction.id == request_params.get('id')).delete()
        mantis_clear_mapping_rule(field, request_params.get('id'))
    elif field == 'fuLi_group':
        MantisFuLiGroup.query.filter(MantisFuLiGroup.id == request_params.get('id')).delete()
        _cascade_clear_fuli()
    elif field == 'fuLi':
        MantisFuLi.query.filter(MantisFuLi.id == request_params.get('id')).update({'delete_flag': 2})
        mantis_clear_mapping_rule(f'{field}_value', request_params.get('id'))
    mantis_db.session.commit()
    mantis_update_field_mapping_rule()
    return 200


def mantis_create_field_value_tool(request_params):
    field = request_params.get('field')
    current_field = MantisCaseField.query.filter(MantisCaseField.case_field == field.lower()).first()
    field_mapping = current_field.case_field_mapping
    key_list = [int(i) for i in field_mapping.keys()]
    key_list.sort()
    new_id = key_list[-1] + 1
    field_mapping[str(new_id)] = request_params.get('field_value')
    MantisCaseField.query.filter(MantisCaseField.case_field == field.lower()).update({
        'case_field_mapping': field_mapping
    })
    mantis_db.session.commit()
    mantis_update_field_mapping_rule()


def mantis_edit_field_value_tool(request_params):
    field = request_params.get('field')
    field_id = request_params.get('field_id')
    current_field = MantisCaseField.query.filter(MantisCaseField.case_field == field.lower()).first()
    field_mapping = current_field.case_field_mapping
    field_mapping[str(field_id)] = request_params.get('field_value')
    MantisCaseField.query.filter(MantisCaseField.case_field == field.lower()).update({
        'case_field_mapping': field_mapping
    })
    mantis_db.session.commit()
    mantis_update_field_mapping_rule()


def mantis_delete_field_value_tool(request_params):
    field = request_params.get('field')
    field_id = request_params.get('field_id')
    current_field = MantisCaseField.query.filter(MantisCaseField.case_field == field.lower()).first()
    field_mapping = current_field.case_field_mapping
    del field_mapping[str(field_id)]
    MantisCaseField.query.filter(MantisCaseField.case_field == field.lower()).update(field_mapping)
    mantis_clear_mapping_rule(field, field_id)
    mantis_db.session.commit()
    mantis_update_field_mapping_rule()


def mantis_clear_mapping_rule(field, field_id):
    mrs = MantisMappingRule.query.filter().all()
    update_list = []
    for mr in mrs:
        mapping_rule = mr.mapping_rule
        if int(field_id) not in mapping_rule.get(field, []):
            continue
        mapping_rule[field].remove(int(field_id))
        update_list.append({
            'id': mr.id,
            'mapping_rule': mapping_rule
        })
    if update_list:
        mantis_db.session.bulk_update_mappings(MantisMappingRule, update_list)


def mantis_check_field_value_tool(request_params):
    field = request_params.get('field')
    field_value = str(request_params.get('field_value')).lower()
    if field.endswith('group'):
        return mantis_check_group_value(field, field_value)
    function_id = request_params.get('function_id')
    field_mapping = json.loads(op11_redis_client.get('field_value2id'))
    filed_value_mapping = field_mapping.get(field)
    if filed_value_mapping.get(str(function_id)):
        filed_value_mapping = filed_value_mapping.get(str(function_id))
    if filed_value_mapping.get(field_value):
        return False
    return True


def mantis_check_group_value(field, field_value):

    def _get_group_name(_group):
        return _group.group_name.lower() if field == 'group' else _group.fuLi_group_name.lower()

    model_dict = {
        'group': Group,
        'fuLi_group': MantisFuLiGroup
    }
    groups = model_dict.get(field).query.filter().all()
    for group in groups:
        if _get_group_name(group) == field_value:
            return False
    return True


def generate_check_field(field):
    if field == 'fuLi':
        return f'{field}_id', f'{field}_id'
    elif field.endswith('function'):
        return field, f'{field}_name'
    else:
        return f'{field}_name', f'{field}_name'


def mantis_check_function_exists_tool(model, key, field, value):
    count = model.get(key).query.filter(getattr(model, field) == value).count()
    return True if count > 0 else False


def mantis_check_function_used_tool(field, value):
    flag = True
    if field == 'function':
        count_1 = SubFunction.query.filter(SubFunction.function == value).count()
        count_2 = TestCase.query.filter(TestCase.function == value).count()
        if count_1 == 0 and count_2 == 0:
            flag = False
    elif field.endswith('sub_function'):
        count_1 = TestCase.query.filter(TestCase.sub_function == value).count()
        if count_1 == 0:
            flag = False
    elif field.endswith('fuLi_group'):
        count_1 = MantisFuLi.query.filter(MantisFuLi.fuLi_group_id == value).count()
        if count_1 == 0:
            flag = False
    elif field.endswith('fuLi'):
        count_1 = TestCase.query.filter(TestCase.fuLi_id == value).count()
        if count_1 == 0:
            flag = False
    return flag
