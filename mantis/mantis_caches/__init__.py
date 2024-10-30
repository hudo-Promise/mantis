import json
import traceback

from common_tools.tools import create_connection, async_task, op11_redis_client, global_logger
from config.basic_setting import TIMEOUT, mysql_config

from mantis.mantis_caches.activate_tool import activate_case_result, activate_group, activate_func, \
    activate_sub_func, activate_test_case, activate_sw_map, activate_fuli, activate_field, activate_mapping_rule, \
    activate_single_test_case, get_case_result_by_id, activate_single_case_result


@async_task
def activate_cache():
    mantis_mysql_config = mysql_config('mantis')
    conn, curr = create_connection(mantis_mysql_config)

    try:
        global_logger.info('Activating mantis cache ...')
        mantis_init_field(curr)
        mantis_init_test_case_cache(curr)
        mantis_init_mapping_rule(curr)
        op11_redis_client.set('sw_map', json.dumps(activate_sw_map(curr)), ex=TIMEOUT)
        global_logger.info('Activate mantis cache success !')
    except Exception as e:
        global_logger.error(e)
        global_logger.error(traceback.print_exc())
    finally:
        curr.close()
        conn.close()


def mantis_update_cache():
    mantis_mysql_config = mysql_config('mantis')
    conn, curr = create_connection(mantis_mysql_config)
    try:
        mantis_init_test_case_cache(curr)
    except Exception as e:
        print(e)
    finally:
        curr.close()
        conn.close()


def mantis_get_single_cache(case_id):
    """
    获取case原始缓存信息
    """
    mantis_mysql_config = mysql_config('mantis')
    conn, curr = create_connection(mantis_mysql_config)
    try:
        cluster, case_info = activate_single_test_case(curr, case_id)
        return cluster, case_info
    except Exception as e:
        print(e)
    finally:
        curr.close()
        conn.close()


def mantis_get_single_result_cache(result_id=None,case_id=None):
    """
    获取result原始缓存信息
    """
    mantis_mysql_config = mysql_config('mantis')
    conn, curr = create_connection(mantis_mysql_config)
    try:
        if result_id:
            result_unique_id, current_result = get_case_result_by_id(curr, result_id)
            return result_unique_id, current_result
        if case_id:
            case_result, key_result = activate_single_case_result(curr, case_id)
            return key_result
    except Exception as e:
        print(e)
    finally:
        curr.close()
        conn.close()


def mantis_update_single_cache(case_id, update_method='create', origin_cache='', result_unique_id=''):
    """
    单个case缓存信息更新
    update_method: create, update, delete
    """
    mantis_mysql_config = mysql_config('mantis')
    conn, curr = create_connection(mantis_mysql_config)
    try:
        mantis_update_case_cache(curr, case_id, update_method=update_method, origin_cache=origin_cache,
                                 result_unique_id=result_unique_id)
    except Exception as e:
        print(e)
    finally:
        curr.close()
        conn.close()


@async_task
def mantis_update_sw_cache():
    mantis_mysql_config = mysql_config('mantis')
    conn, curr = create_connection(mantis_mysql_config)
    try:
        op11_redis_client.set('sw_map', json.dumps(activate_sw_map(curr)), ex=TIMEOUT)
    except Exception as e:
        print(e)
    finally:
        curr.close()
        conn.close()


def mantis_get_case_cache(curr, case_id):
    """获取case原始缓存"""
    cluster, case_info = activate_single_test_case(curr, case_id)
    return cluster, case_info


def mantis_update_case_cache(curr, case_id, update_method='create', origin_cache='', result_unique_id=''):
    """单个case缓存维护"""
    if update_method == 'create':
        # 创建需要添加test_case_cache exists_case
        cluster, case_info = activate_single_test_case(curr, case_id)
        op11_redis_client.lpush(f'test_case_cache_{cluster}', case_info)
        op11_redis_client.hset('exists_case', case_id, case_id)
    elif update_method == 'update' and origin_cache != '':
        cluster, origin_case_info = origin_cache
        # 编辑需要先删除test_case_cache中信息并重新添加
        op11_redis_client.lrem(f'test_case_cache_{cluster}', 1, origin_case_info)
        cluster, case_info = activate_single_test_case(curr, case_id)
        op11_redis_client.lpush(f'test_case_cache_{cluster}', case_info)
    elif update_method == 'delete' and origin_cache != '':
        # 删除需要删除 test_case_cache exists_case exists_result 中保存的信息
        cluster, origin_case_info = origin_cache
        op11_redis_client.lrem(f'test_case_cache_{cluster}', 1, origin_case_info)
        op11_redis_client.hdel('exists_case', case_id)
        if result_unique_id:
            for key in result_unique_id:
                op11_redis_client.hdel('exists_result', key)
    elif update_method == 'delete result' and origin_cache != '':
        # 删除需要删除exists_result 中保存的信息并更新test_case_cache中缓存信息
        origin_cluster, origin_case_info = origin_cache
        cluster, case_info = activate_single_test_case(curr, case_id)
        op11_redis_client.linsert(f'test_case_cache_{cluster}', 'BEFORE', origin_case_info, case_info)
        op11_redis_client.lrem(f'test_case_cache_{cluster}', 1, origin_case_info)
        if result_unique_id:
            op11_redis_client.hdel('exists_result', result_unique_id)


def mantis_init_test_case_cache(curr):
    lock_key = 'mantis_key'
    lock_acquired = op11_redis_client.set(lock_key, "locked", nx=True, ex=10)
    if lock_acquired:
        try:
            cluster_dict = json.loads(op11_redis_client.get('field_id2value')).get('cluster')
            key_list = ['exists_case', 'exists_result'] + [f'test_case_cache_{cluster}' for cluster in cluster_dict.keys()]
            op11_redis_client.delete(*key_list)
            test_case_cache, exists_case_dict, exists_result_dict = activate_test_case(curr, cluster_dict)
            for cluster, cases in test_case_cache.items():
                if not cases:
                    continue
                op11_redis_client.lpush(f'test_case_cache_{cluster}', *cases)
            op11_redis_client.hmset('exists_case', exists_case_dict)
            op11_redis_client.hmset('exists_result', exists_result_dict)
        finally:
            op11_redis_client.delete(lock_key)


def mantis_init_fuli(curr):
    fuli_value2id, fuli_id2value, fuli_groups = activate_fuli(curr)
    op11_redis_client.set('fuLi_group', json.dumps(fuli_groups), ex=TIMEOUT)
    return fuli_value2id, fuli_id2value


def mantis_init_field(curr):
    op11_redis_client.set('group', json.dumps(activate_group(curr)), ex=TIMEOUT)
    field_id2value, field_value2id = activate_field(curr)
    fuli_value2id, fuli_id2value = mantis_init_fuli(curr)
    field_id2value['fuLi_value'] = fuli_id2value
    field_value2id['fuLi_value'] = fuli_value2id
    function_id2value, function_value2id = activate_func(curr)
    field_id2value['function'] = function_id2value
    field_value2id['function'] = function_value2id
    sub_function_id2value, sub_function_value2id, sub_func_id2func_id = activate_sub_func(curr)
    field_id2value['sub_function'] = sub_function_id2value
    field_id2value['sub_func_id2func_id'] = sub_func_id2func_id
    field_value2id['sub_function'] = sub_function_value2id
    op11_redis_client.set('field_id2value', json.dumps(field_id2value), ex=TIMEOUT)
    op11_redis_client.set('field_value2id', json.dumps(field_value2id), ex=TIMEOUT)


def mantis_init_mapping_rule(curr):
    cluster_config_mapping = activate_mapping_rule(curr, json.loads(op11_redis_client.get('field_id2value')))
    op11_redis_client.set('mapping_rule', json.dumps(cluster_config_mapping), ex=TIMEOUT)


@async_task
def mantis_update_field_mapping_rule():
    mantis_mysql_config = mysql_config('mantis')
    conn, curr = create_connection(mantis_mysql_config)
    try:
        mantis_init_field(curr)
        mantis_init_mapping_rule(curr)
    except Exception as e:
        print(e)
    finally:
        curr.close()
        conn.close()
