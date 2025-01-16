# -*- coding: utf-8 -*-
import json
import re

import xlrd

from common_tools.tools import create_current_format_time, op11_redis_client
from mantis.mantis_status import column_no, column_rule, matrix_rule, case_col, case_result_col, unique_col


def data_classification(content, mode):
    error_data_info = []
    insert_list = []
    upgrade_list = []
    not_update = []
    update_case_upgrade_time_list = []
    status, pre_result_mapping = verification_preprocessing(content)
    if not status:
        return status, pre_result_mapping
    if mode == 'upload_case':
        get_upload_case_info(pre_result_mapping, error_data_info, insert_list, upgrade_list, not_update)
    elif mode == 'upload_sw':
        get_upload_sw_info(
            pre_result_mapping, error_data_info, insert_list, upgrade_list, update_case_upgrade_time_list
        )
    if error_data_info:
        return False, {'error_type': 'error_value', 'error_info': error_data_info}
    if not_update:
        return False, {'error_type': 'not_exists_row', 'error_info': not_update}
    return True, {
        'insert_list': insert_list,
        'upgrade_list': upgrade_list,
        'update_case_upgrade_time_list': update_case_upgrade_time_list
    }


def verification_preprocessing(content):
    data = xlrd.open_workbook(file_contents=content)
    try:
        table = data.sheet_by_index(0)
    except Exception as e:
        print(e)
        return False, {'error_type': 'Sheet', 'error_info': None}
    rows = table.nrows
    cols = table.ncols

    if rows == 0 and cols == 0:
        return False, {'error_type': 'Sheet', 'error_info': None}
    error_data_info = []
    if cols != 35:
        for i in range(0, rows):
            for j in range(0, cols):
                error_data_info.append([i, j, None])
        return False, {'error_type': 'redundant_column', 'error_info': error_data_info}
    duplicate_case = {}
    for row in range(1, rows):
        m_id = table.cell(row, 0).value
        if str(m_id).lower() != 'new':
            if m_id in duplicate_case.keys():
                duplicate_case[m_id].append(row + 1)
            else:
                duplicate_case[m_id] = [row + 1]
    for key, value in duplicate_case.items():
        if len(value) > 1:
            error_data_info.append(value)
    if error_data_info:
        return False, {'error_type': 'duplicate_row', 'error_info': error_data_info}
    else:
        return True, {
            'table': table,
            'sw_map': json.loads(op11_redis_client.get('sw_map')),
            'field_value2id': json.loads(op11_redis_client.get('field_value2id')),
            'exists_case': op11_redis_client.hkeys('exists_case'),
            'exists_result': op11_redis_client.hgetall('exists_result'),
            'user_account2id': json.loads(op11_redis_client.get('user_account2id')),
            'rows': rows,
            'cols': cols
        }


def get_upload_case_info(mapping, error_data_info, insert_list, upgrade_list, not_update):
    current_time = create_current_format_time()
    for row, row_values in case_iterator(mapping.get('table'), mapping.get('rows'), mapping.get('cols')):
        row_dict = {'upgrade_time': current_time}
        for col in case_col:
            value = case_value_pre_deal(row_values, col)
            flag = True
            if column_rule.get(col) == 'check_mid':
                flag = check_mid(value)
            elif column_rule.get(col) == 'field_single':
                field_mapping = mapping.get('field_value2id').get(column_no.get(col))
                if column_no.get(col) == 'sub_function':
                    field_mapping = field_mapping.get(str(row_dict.get('function')))
                flag, value = field_single(value, field_mapping)
            elif column_rule.get(col) == 'field_more':
                flag, value = field_more(value, mapping.get('field_value2id').get(column_no.get(col)))
            elif column_rule.get(col) == 'not_null':
                flag = not is_null(value)
            elif column_rule.get(col) == 'user_account':
                flag, value = user_account(value, mapping.get('user_account2id'))
            if not flag:
                error_data_info.append([row, col, value])
                continue
            row_dict[column_no[col] if column_no[col] != 'fuLi_value' else 'fuLi_id'] = value

        if isinstance(row_dict.get('m_id'), str) and row_dict.get('m_id').lower() == 'new':
            row_dict['create_time'] = current_time
            row_dict['delete_flag'] = 0
            del row_dict['m_id']
            insert_list.append(row_dict)
        else:
            if row_dict.get('m_id') not in mapping.get('exists_case'):
                not_update.append(row)
                continue
            row_dict['id'] = row_dict.get('m_id')
            del row_dict['m_id']
            upgrade_list.append(row_dict)


def get_upload_sw_info(mapping, error_data_info, insert_list, upgrade_list, update_case_upgrade_time):
    current_time = create_current_format_time()
    for row, row_values in case_iterator(mapping.get('table'), mapping.get('rows'), mapping.get('cols')):
        m_id = case_value_pre_deal(row_values, 0)
        if m_id == 'new':
            error_data_info.append([row, 0, 'new'])
            continue
        matrix, result_unique_id, current_result_dict = generate_case_result_matrix(
            m_id, row_values, field_mapping=mapping.get('field_value2id'))
        if matrix not in matrix_rule:
            for col in case_result_col[:10]:
                error_data_info.append([row, col, case_value_pre_deal(row_values, col)])
            continue
        if matrix.startswith('null'):
            continue
        tester = case_value_pre_deal(row_values, 30)
        flag, value = user_account(tester, mapping.get('user_account2id'))
        current_result_dict['tester'] = tester
        if not flag:
            error_data_info.append([row, 30, tester])
            continue
        cycle_id = case_value_pre_deal(row_values, 31)
        flag = check_mid(cycle_id)
        current_result_dict['cycle_id'] = cycle_id
        if not flag:
            error_data_info.append([row, 31, cycle_id])
            continue
        if result_unique_id in mapping.get('exists_result').keys():
            current_result_dict['upgrade_time'] = current_time
            current_result_dict['id'] = mapping.get('exists_result').get(result_unique_id)
            upgrade_list.append(current_result_dict)
        else:
            current_result_dict['create_time'] = current_time
            current_result_dict['upgrade_time'] = current_time
            current_result_dict['sw_num'] = generate_sw_num(current_result_dict.get('test_sw'), mapping.get('sw_map'))
            current_result_dict['m_id'] = int(m_id)
            insert_list.append(current_result_dict)
        update_case_upgrade_time.append({'id': m_id, 'upgrade_time': current_time})


def generate_case_result_matrix(m_id, row_values, field_mapping=None, mode=None):
    current_result_dict = {column_no.get(col): case_value_pre_deal(row_values, col) for col in case_result_col}
    result_unique_id = str(m_id)
    matrix = None
    if not mode:
        matrix = (
            f'{check_sw(current_result_dict.get("test_sw"))}_'
            f'{check_result(current_result_dict.get("test_result"), field_mapping.get("test_result"))}_'
            f'{check_test(current_result_dict.get("test_platform"), field_mapping.get("test_platform"))}_'
            f'{check_test(current_result_dict.get("test_carline"), field_mapping.get("test_carline"))}_'
            f'{check_test(current_result_dict.get("test_variant"), field_mapping.get("test_variant"))}_'
            f'{check_test(current_result_dict.get("test_market"), field_mapping.get("test_market"))}_'
            f'{check_test(current_result_dict.get("test_language"), field_mapping.get("test_language"))}_'
            f'{check_test(current_result_dict.get("test_environment"), field_mapping.get("test_environment"))}_'
            f'{check_tb_type(current_result_dict.get("tb_type"), field_mapping.get("tb_type"))}_'
            f'{check_issue_descr(current_result_dict.get("issue_descr"))}'
        )
    for key in current_result_dict.keys():
        if not field_mapping.get(key):
            continue
        current_result_dict[key] = field_mapping.get(key).get(current_result_dict.get(key))
    for key in unique_col:
        if not current_result_dict.get(key):
            continue
        result_unique_id = '_'.join([result_unique_id, current_result_dict.get(key)])
    if mode == "delete":
        return matrix, result_unique_id, None
    return matrix, result_unique_id, current_result_dict


def case_iterator(table, rows, cols):
    for row in range(1, rows):
        yield row, table.row_values(rowx=row, start_colx=0, end_colx=cols)


def case_value_pre_deal(value_list, col):
    if isinstance(value_list[col], str):
        value = value_list[col].strip().lower()
    elif isinstance(value_list[col], float):
        value = str(int(value_list[col]))
    else:
        value = value_list[col]
    return value


def is_digit(value, lens=None):
    if not value.isdigit():
        return False
    if lens is not None and len(value) != lens:
        return False
    return True


def check_mid(value):
    return True if is_digit(value) or value == 'new' else False


def field_single(field_value, field_mapping):
    if not field_mapping:
        return False, None
    digit_value = field_mapping.get(field_value)
    if digit_value is None:
        return False, digit_value
    else:
        return True, int(digit_value)


def field_more(field_value, field_mapping):
    """
    特定字符不为空 (多个值)
    """
    values = []
    if ',' in field_value:
        values = field_value.strip().split(',')
    elif '\n' in field_value:
        values = field_value.strip().split('\n')
    else:
        values.append(field_value)
    field_list = []
    for value in values:
        if field_mapping.get(value) is None:
            return False, None
        field_list.append(int(field_mapping.get(value)))
    return True, field_list


def user_account(value, account2id):
    if account2id.get(value):
        return True, account2id[value]
    else:
        return False, None


def is_null(value, mode=None):
    if mode:
        return True if value else False
    return True if value == 'null' else False


def check_sw(value):
    if is_null(value, mode=False):
        return value
    pattern = re.compile(r'^[a-zA-Z]\d{3,4}$')
    num_pattern = re.compile(r'^\d{4}$')
    return 'string' if pattern.match(str(value)) or num_pattern.match(str(value)) else 'fake'


def check_test(field_value, field_mapping):
    if is_null(field_value, mode=False):
        return field_value
    return 'string' if field_mapping.get(field_value) else 'fake'


def check_tb_type(field_value, field_mapping):
    if not field_mapping.get(field_value):
        return 'fake'
    return field_value if field_value in ['null', 'ticket'] else 'string'


def check_result(field_value, field_mapping):
    return field_value if field_mapping.get(field_value) else 'fake'


def check_issue_descr(value):
    if value == 'null':
        return value
    if is_digit(value, lens=7):
        return str(7)
    if is_digit(value, lens=8):
        return str(8)
    return 'unlimited'


def get_delete_unique_id(content, mode):
    ok, result_mapping = verification_preprocessing(content)
    if not ok:
        return False, result_mapping.get('error_info'), result_mapping.get('error_type')
    unique_id_list = []
    not_exists_list = []
    for row, row_values in case_iterator(
            result_mapping.get('table'), result_mapping.get('rows'), result_mapping.get('cols')
    ):
        case_id = case_value_pre_deal(row_values, 0)
        if mode == 'delete_case':
            if str(case_id) not in result_mapping.get('exists_case'):
                not_exists_list.append(row)
                continue
            unique_id_list.append(int(case_id))
        elif mode == 'delete_sw':
            _, result_unique_id, _ = generate_case_result_matrix(
                case_id, row_values, result_mapping.get('field_value2id'), mode='delete'
            )
            if result_unique_id not in result_mapping.get('exists_result').keys():
                not_exists_list.append(row)
                continue
            unique_id_list.append(result_mapping.get('exists_result').get(result_unique_id))
    if not_exists_list:
        return False, not_exists_list, 'not_exists_row'
    return True, unique_id_list, None


def generate_sw_num(sw, sw_map):
    sw_num = ''
    for i in sw:
        if i.isalpha():
            if sw_map.get(i) is not None:
                sw_num += str(sw_map.get(i))
            else:
                pass
        else:
            sw_num += i
    return int(sw_num) if sw_num else int(sw)
