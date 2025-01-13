from config.basic_setting import VERSION

column_no = {
    0: 'm_id',
    1: 'category',
    2: 'function',
    3: 'sub_function',
    4: 'fuLi_value',
    5: 'level',
    6: 'cluster',

    7: 'available_platform',
    8: 'available_carline',
    9: 'available_variant',
    10: 'available_market',
    11: 'available_language',
    12: 'available_environment',

    13: 'title',
    14: 'precondition',
    15: 'action',
    16: 'expectation',
    28: 'reference spec',

    17: 'test_sw',
    18: 'test_result',
    19: 'test_platform',
    20: 'test_carline',
    21: 'test_variant',
    22: 'test_market',
    23: 'test_language',
    24: 'test_environment',
    25: 'tb_type',
    26: 'issue_descr',
    27: 'comments',
    29: 'extra_1',
    30: 'extra_2',
    31: 'extra_3',
}


column_rule = {
    0: 'check_mid',
    1: 'field_single',
    2: 'field_single',
    3: 'field_single',
    4: 'field_single',
    5: 'field_single',
    6: 'field_single',
    7: 'field_more',
    8: 'field_more',
    9: 'field_more',
    10: 'field_more',
    11: 'field_more',
    12: 'field_more',
    13: 'not_null',
    14: 'not_null',
    15: 'not_null',
    16: 'not_null',
    27: 'unlimited',

    17: 'check_sw',
    18: 'check_result',
    19: 'check_test',
    20: 'check_test',
    21: 'check_test',
    22: 'check_test',
    23: 'check_test',
    24: 'check_test',

    26: 'check_issue_descr',
}


matrix_rule = [
    'null_null_null_null_null_null_null_null_null_null',
    'string_null_string_string_string_string_string_string_null_null',
    'string_pass_string_string_string_string_string_string_null_null',
    'string_fail_string_string_string_string_string_string_null_7',
    'string_tb_string_string_string_string_string_string_ticket_7',
    'string_fail_string_string_string_string_string_string_null_8',
    'string_tb_string_string_string_string_string_string_ticket_8',
    'string_tb_string_string_string_string_string_string_string_unlimited',
    'string_n/a_string_string_string_string_string_string_null_null',
]


case_col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 28]


case_result_col = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31]

unique_col = [
    'test_sw',
    'test_platform',
    'test_carline',
    'test_variant',
    'test_market',
    'test_language',
    'test_environment'
]


table_head = [
    'M-ID',
    'Category',
    'Function',
    'Sub Function',
    'Fuli ID',
    'Level',
    'Cluster',
    'Available Platform',
    'Available Carline',
    'Available Variant',
    'Available Market',
    'Available Language',
    'Available Environment',
    'Test Case Description/Title',
    'Precondition',
    'Action',
    'Expectation',
    'Test SW',
    'Test Result',
    'Test Platform',
    'Test Carline',
    'Test Variant',
    'Test Market',
    'Test Language',
    'Test Environment',
    'TB Type',
    'Issue Descr',
    'Comments',
    'Reference Spec',
    'Extra 1',
    'Extra 2',
    'Extra 3'
]  # len == 32


key_list = [
    'm_id',
    'category',
    'function',
    'sub_function',
    'fuLi_value',
    'level',
    'cluster',
    'available_platform',
    'available_carline',
    'available_variant',
    'available_market',
    'available_language',
    'available_environment',
    'title',
    'precondition',
    'action',
    'expectation',
    'test_sw',
    'test_result',
    'test_platform',
    'test_carline',
    'test_variant',
    'test_market',
    'test_language',
    'test_environment',
    'tb_type',
    'issue_descr',
    'comments',
    'reference_spec',
    'extra_1',
    'extra_2',
    'extra_3'
]


mantis_project = {
    1: 'HCP3',
    2: 'OCI@A',
}

mantis_project_to_cluster = {
    1: [1, 4],
    2: [6, 7, 8, 9],
}


user_operate_record_url_list = [
    f'/{VERSION}/mantis/upload',
    f'/{VERSION}/mantis/delete/case',

    f'/{VERSION}/mantis/create/functions',
    f'/{VERSION}/mantis/edit/functions',
    f'/{VERSION}/mantis/delete/functions',

    f'/{VERSION}/mantis/create/field/value',
    f'/{VERSION}/mantis/edit/field/value',
    f'/{VERSION}/mantis/delete/field/value',

    f'/{VERSION}/mantis/create/mapping/rule',
    f'/{VERSION}/mantis/edit/mapping/rule',
    f'/{VERSION}/mantis/delete/mapping/rule',
    f'/{VERSION}/mantis/clone/mapping/rule',
]


field_display_order = {
    'case': [
        'category',
        'level',
        'available_platform',
        'available_carline',
        'available_variant',
        'available_market',
        'available_language',
        'available_environment'
    ],
    'result': [
        'category',
        'level',
        'test_result',
        'tb_type',
        'test_platform',
        'test_carline',
        'test_variant',
        'test_market',
        'test_language',
        'test_environment'
    ]
}


test_case_key = [
    'case_id',
    'category',
    'sub_function',
    'level',
    'available_platform',
    'available_carline',
    'available_variant',
    'available_market',
    'available_language',
    'available_environment',
    'fuLi_value'
]


test_case_param = [
    'm_id',
    'title',
    'precondition',
    'action',
    'expectation'
]


case_result_key = [
    'test_variant',
    'test_carline',
    'test_market',
    'test_platform',
    'test_language',
    'test_environment',
    'test_sw',
    'test_result',
    'tb_type',
    'issue_descr',
    'comments',
    'extra_1',
    'extra_2',
    'extra_3'
]


case_result_param = [
    'test_sw',
    'issue_descr',
    'comments'
]


milestone_status = {
    1: 'To Do',
    2: 'In Progress',
    3: 'Done',
}


cycle_status = {
    1: 'To Do',
    2: 'In Queue',
    3: 'In Progress',
    4: 'Done',
}

free_test_status = {
    1: 'Open',
    2: 'In Progress',
    3: 'Test OK',
    4: 'Test NOK',
    5: 'Test Blocked'
}

label_mapping = {
    1: 'Normal',
    2: 'Risk',
    3: 'Delay',
}


status_template = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0
}


mtc_groups = [2, 3, 4, 5, 6, 7]
