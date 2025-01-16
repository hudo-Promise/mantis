# -*- coding: utf-8 -*-
import json


def activate_test_case(curr, cluster_dict):
    test_case_sql = """
        select
            `id`,
            `creator`,
            `category`,
            `function`,
            `sub_function`,
            `fuLi_id`,
            `level`,
            `cluster`,
            `available_platform`,
            `available_carline`,
            `available_variant`,
            `available_market`,
            `available_language`,
            `available_environment`,
            `title`,
            `precondition`,
            `action`,
            `expectation`,
            `reference_spec`,
            `create_time`,
            `upgrade_time`
        from
            test_case
        where
            delete_flag = 0
        order by
            upgrade_time
    """
    curr.execute(test_case_sql)
    test_case = curr.fetchall()
    test_case_cache = {int(i): [] for i in cluster_dict.keys()}
    exists_case_dict = {}
    case_result_dict, exists_result_dict = activate_case_result(curr)
    for case in test_case:
        test_case = generate_current_case_dict(case, case_result_dict.get(case.get('id')))
        test_case_cache.get(case.get('cluster')).append(json.dumps(test_case))
        exists_case_dict[case.get('id')] = case.get('id')
    return test_case_cache, exists_case_dict, exists_result_dict


def activate_single_test_case(curr, case_id):
    test_case_sql = """
        select
            `id`,
            `creator`,
            `category`,
            `function`,
            `sub_function`,
            `fuLi_id`,
            `level`,
            `cluster`,
            `available_platform`,
            `available_carline`,
            `available_variant`,
            `available_market`,
            `available_language`,
            `available_environment`,
            `title`,
            `precondition`,
            `action`,
            `expectation`,
            `reference_spec`,
            `create_time`,
            `upgrade_time`
        from
            test_case
        where
            delete_flag = 0 and id = %s
        order by
            upgrade_time
    """
    curr.execute(test_case_sql, (case_id,))
    test_case = curr.fetchall()
    case_result, key_result = activate_single_case_result(curr, case_id)
    if test_case:
        test_case = generate_current_case_dict(test_case[0], case_result)
        return test_case.get('cluster'), json.dumps(test_case)
    else:
        return '', ''


def generate_current_case_dict(case, case_result_dict):
    current_case_dict = {
        'm_id': case.get('id'),
        'creator': case.get('creator'),
        'category': case.get('category'),
        'function': case.get('function'),
        'sub_function': case.get('sub_function'),
        'fuLi_value': case.get('fuLi_id'),
        'level': case.get('level'),
        'cluster': case.get('cluster'),
        'available_platform': json.loads(case.get('available_platform')),
        'available_carline': json.loads(case.get('available_carline')),
        'available_variant': json.loads(case.get('available_variant')),
        'available_market': json.loads(case.get('available_market')),
        'available_language': json.loads(case.get('available_language')),
        'available_environment': json.loads(case.get('available_environment')),
        'title': case.get('title'),
        'precondition': case.get('precondition'),
        'action': case.get('action'),
        'expectation': case.get('expectation'),
        'reference_spec': case.get('reference_spec'),
        'create_time': str(case.get('create_time')),
        'upgrade_time': str(case.get('upgrade_time')),
        'case_result': case_result_dict,
    }
    return current_case_dict


def activate_case_result(curr):
    case_result_sql = """
        select 
            `id`,
            `m_id`,
            `test_sw`,
            `test_result`,
            `test_platform`,
            `test_carline`,
            `test_variant`,
            `test_market`,
            `test_language`,
            `test_environment`,
            `tb_type`,
            `issue_descr`,
            `comments`,
            `tester`,
            `cycle_id`,
            `extra_1`,
            `extra_2`,
            `extra_3`,
            `create_time`,
            `upgrade_time`
        from 
            case_result
        order by `m_id` asc, `sw_num` asc, `upgrade_time` desc
    """
    curr.execute(case_result_sql)
    case_results = curr.fetchall()
    result = {}
    exists_result = {}
    unique_key = [
        'm_id', 'test_sw', 'test_platform', 'test_carline', 'test_variant', 'test_market',
        'test_language', 'test_environment'
    ]
    for case_result in case_results:
        current_result = {
            'case_result_id': case_result.get('id'),
            'm_id': case_result.get('m_id'),
            'test_sw': case_result.get('test_sw'),
            'test_result': case_result.get('test_result'),
            'test_platform': case_result.get('test_platform'),
            'test_carline': case_result.get('test_carline'),
            'test_variant': case_result.get('test_variant'),
            'test_market': case_result.get('test_market'),
            'test_language': case_result.get('test_language'),
            'test_environment': case_result.get('test_environment'),
            'tb_type': case_result.get('tb_type'),
            'issue_descr': case_result.get('issue_descr'),
            'comments': case_result.get('comments'),
            'extra_1': case_result.get('extra_1'),
            'extra_2': case_result.get('extra_2'),
            'extra_3': case_result.get('extra_3'),
            'tester': case_result.get('tester'),
            'cycle_id': case_result.get('cycle_id'),
            'create_time': str(case_result.get('create_time')),
            'upgrade_time': str(case_result.get('upgrade_time')),
        }
        if case_result.get('m_id') not in result.keys():
            result[case_result.get('m_id')] = []
        result[case_result.get('m_id')].append(current_result)
        result_unique_id = '_'.join([str(current_result.get(key)) for key in unique_key])
        if result_unique_id not in exists_result.keys():
            exists_result[result_unique_id] = current_result.get('case_result_id')
    return result, exists_result


def activate_case_result_aug(curr):
    case_result_sql = """
        select `id`, `aug_task_id` from case_result
    """
    curr.execute(case_result_sql)
    case_results = curr.fetchall()
    aug_id_mapping = {case_result.get('aug_task_id'): case_result.get('id') for case_result in case_results}
    return aug_id_mapping


def activate_single_case_result(curr, case_id):
    case_result_sql = """
        select 
            `id`,
            `m_id`,
            `test_sw`,
            `test_result`,
            `test_platform`,
            `test_carline`,
            `test_variant`,
            `test_market`,
            `test_language`,
            `test_environment`,
            `tb_type`,
            `issue_descr`,
            `comments`,
            `extra_1`,
            `extra_2`,
            `extra_3`,
            `create_time`,
            `upgrade_time`
        from 
            case_result
        where
            m_id = %s
        order by `m_id` asc, `sw_num` asc, `upgrade_time` desc
    """
    curr.execute(case_result_sql, (case_id,))
    case_results = curr.fetchall()
    result = []
    key_result = []
    unique_key = [
        'm_id', 'test_sw', 'test_platform', 'test_carline', 'test_variant', 'test_market',
        'test_language', 'test_environment'
    ]
    for case_result in case_results:
        current_result = {
            'case_result_id': case_result.get('id'),
            'm_id': case_result.get('m_id'),
            'test_sw': case_result.get('test_sw'),
            'test_result': case_result.get('test_result'),
            'test_platform': case_result.get('test_platform'),
            'test_carline': case_result.get('test_carline'),
            'test_variant': case_result.get('test_variant'),
            'test_market': case_result.get('test_market'),
            'test_language': case_result.get('test_language'),
            'test_environment': case_result.get('test_environment'),
            'tb_type': case_result.get('tb_type'),
            'issue_descr': case_result.get('issue_descr'),
            'comments': case_result.get('comments'),
            'extra_1': case_result.get('extra_1'),
            'extra_2': case_result.get('extra_2'),
            'extra_3': case_result.get('extra_3'),
            'create_time': str(case_result.get('create_time')),
            'upgrade_time': str(case_result.get('upgrade_time')),
        }
        result_unique_id = '_'.join([str(current_result.get(key)) for key in unique_key])
        key_result.append(result_unique_id)
        result.append(current_result)
    if result:
        return result, key_result
    else:
        return None, None


def get_case_result_by_id(curr, result_id):
    case_result_sql = """
        select 
            `id`,
            `m_id`,
            `test_sw`,
            `test_result`,
            `test_platform`,
            `test_carline`,
            `test_variant`,
            `test_market`,
            `test_language`,
            `test_environment`,
            `tb_type`,
            `issue_descr`,
            `comments`,
            `extra_1`,
            `extra_2`,
            `extra_3`,
            `create_time`,
            `upgrade_time`
        from 
            case_result
        where
            id = %s
        order by `m_id` asc, `sw_num` asc, `upgrade_time` desc
    """
    curr.execute(case_result_sql, (result_id,))
    case_results = curr.fetchall()
    result = {}
    unique_key = [
        'm_id', 'test_sw', 'test_platform', 'test_carline', 'test_variant', 'test_market',
        'test_language', 'test_environment'
    ]
    if case_results:
        case_result = case_results[0]
        current_result = {
            'case_result_id': case_result.get('id'),
            'm_id': case_result.get('m_id'),
            'test_sw': case_result.get('test_sw'),
            'test_result': case_result.get('test_result'),
            'test_platform': case_result.get('test_platform'),
            'test_carline': case_result.get('test_carline'),
            'test_variant': case_result.get('test_variant'),
            'test_market': case_result.get('test_market'),
            'test_language': case_result.get('test_language'),
            'test_environment': case_result.get('test_environment'),
            'tb_type': case_result.get('tb_type'),
            'issue_descr': case_result.get('issue_descr'),
            'comments': case_result.get('comments'),
            'extra_1': case_result.get('extra_1'),
            'extra_2': case_result.get('extra_2'),
            'extra_3': case_result.get('extra_3'),
            'create_time': str(case_result.get('create_time')),
            'upgrade_time': str(case_result.get('upgrade_time')),
        }
        result_unique_id = '_'.join([str(current_result.get(key)) for key in unique_key])
        return result_unique_id, current_result
    else:
        return '', {}


def activate_group(curr):
    group_sql = """
        select id, group_name from `group`
    """
    curr.execute(group_sql)
    group_dict = {}
    group_results = curr.fetchall()
    for group in group_results:
        group_dict[group.get('id')] = group.get('group_name')
    return group_dict


def activate_func(curr):
    function_sql = """
        select id, `function` from `functions`
    """
    curr.execute(function_sql)
    function_results = curr.fetchall()
    function_id2value = {}
    function_value2id = {}
    for function in function_results:
        if not function.get('function'):
            continue
        function_id2value[function.get('id')] = function.get('function')
        function_value2id[function.get('function')] = function.get('id')
    return function_id2value, function_value2id


def activate_sub_func(curr):
    sub_function_sql = """
        select id, `function`, sub_function from `sub_functions`
    """
    curr.execute(sub_function_sql)
    sub_function_results = curr.fetchall()
    sub_function_id2value = {}
    sub_function_value2id = {}
    sub_func_id2func_id = {}

    for sub_function in sub_function_results:
        if not sub_function.get('sub_function'):
            continue
        sub_func_id2func_id[sub_function.get('id')] = sub_function.get('function')
        sub_function_id2value[sub_function.get('id')] = sub_function.get('sub_function')
        if sub_function.get('function') not in sub_function_value2id.keys():
            sub_function_value2id[sub_function.get('function')] = {}
        sub_function_value2id[sub_function.get('function')][sub_function.get('sub_function')] = sub_function.get('id')
    return sub_function_id2value, sub_function_value2id, sub_func_id2func_id


def activate_sw_map(curr):
    sw_map_sql = """
        select `sw_alpha`, sw_num from `sw_map` where delete_flag = 0
    """
    curr.execute(sw_map_sql)
    sw_map_results = curr.fetchall()
    sw_map_dict = {}
    for sw_map in sw_map_results:
        sw_map_dict[sw_map.get('sw_alpha')] = sw_map.get('sw_num')
    return sw_map_dict


def activate_fuli(curr):
    fuli_group_sql = """
        select id, fuLi_group_name from `mantis_fuLi_group`
    """
    curr.execute(fuli_group_sql)
    fuli_group_results = curr.fetchall()
    fuli_groups = {}
    for fuli_group in fuli_group_results:
        if fuli_group.get('id') not in fuli_group.keys():
            fuli_group['fuLi'] = {}
        fuli_groups[fuli_group.get('id')] = fuli_group

    fu_li_sql = """
        select id as fuLi_value, fuLi_id, fuLi_desc, fuLi_group_id from `mantis_fuLi` where delete_flag = 1
    """
    curr.execute(fu_li_sql)
    fu_li_results = curr.fetchall()
    fuli_value2id = {}
    fuli_id2value = {}
    for fu_li in fu_li_results:
        fuli_value2id[fu_li.get('fuLi_id')] = fu_li.get('fuLi_value')
        fuli_id2value[fu_li.get('fuLi_value')] = fu_li.get('fuLi_id')
        if not fuli_groups.get(fu_li.get('fuLi_group_id')):
            continue
        fuli_groups[fu_li.get('fuLi_group_id')]['fuLi'][fu_li.get('fuLi_value')] = fu_li
    return fuli_value2id, fuli_id2value, fuli_groups


def activate_field(curr):
    field_sql = """
        select id, case_field, case_field_mapping from `mantis_case_field`
    """
    curr.execute(field_sql)
    field_results = curr.fetchall()
    field_id2value = {}
    field_value2id = {}
    for field in field_results:
        field_id2value[field.get('case_field')] = json.loads(field.get('case_field_mapping'))
        field_value2id[field.get('case_field')] = generate_field_value2id_mapping(field.get('case_field_mapping'))
    return field_id2value, field_value2id


def generate_field_value2id_mapping(case_field_mapping):
    field_mapping = {}
    for key, value in json.loads(case_field_mapping).items():
        field_mapping[value.lower()] = key
    return field_mapping


def activate_mapping_rule(curr, field_mapping):
    cluster_config_sql = """
        select cluster_id, mapping_rule from `mantis_mapping_rule`
    """
    curr.execute(cluster_config_sql)
    cluster_config_results = curr.fetchall()
    cluster_config_mapping = {}
    for item in cluster_config_results:
        if not item.get('cluster_id'):
            continue
        if item.get('cluster_id') not in cluster_config_mapping.keys():
            cluster_config_mapping[item.get('cluster_id')] = {'id2value': {}, 'value2id': {}}
        generate_field_mapping(cluster_config_mapping, item, field_mapping)
    return cluster_config_mapping


def generate_field_mapping(cluster_config_mapping, cluster_config, field_mapping):
    for key, value in json.loads(cluster_config.get('mapping_rule')).items():
        if not value:
            cluster_config_mapping[cluster_config.get('cluster_id')]['id2value'][key] = {}
        else:
            cluster_config_mapping[
                cluster_config.get('cluster_id')
            ]['id2value'][key] = {i: field_mapping.get(key).get(str(i)) for i in value}

        if key != 'sub_function':
            if not value:
                cluster_config_mapping[cluster_config.get('cluster_id')]['value2id'][key] = {}
            else:
                cluster_config_mapping[
                    cluster_config.get('cluster_id')
                ]['value2id'][key] = {field_mapping.get(key).get(str(i)).lower(): i for i in value}
        else:
            cluster_config_mapping[cluster_config.get('cluster_id')]['value2id'][key] = {}
            if value:
                for i in value:
                    func_id = field_mapping.get('sub_func_id2func_id').get(str(i))
                    if func_id not in cluster_config_mapping[cluster_config.get('cluster_id')]['value2id'][key].keys():
                        cluster_config_mapping[cluster_config.get('cluster_id')]['value2id'][key][func_id] = {}
                    cluster_config_mapping[
                        cluster_config.get('cluster_id')
                    ]['value2id'][key][func_id][field_mapping.get(key).get(str(i)).lower()] = i
