import pymysql

from mantis_sql import (
    create_mantis_board_sql, create_mantis_functions_sql, create_mantis_group_sql, create_mantis_card_group_sql,
    create_mantis_sw_map_sql, create_mantis_fuLi_sql, create_mantis_case_field_sql, create_mantis_test_case_sql,
    create_mantis_case_result_sql, create_mantis_fuLi_group_sql, create_mantis_filter_record_sql,
    create_mantis_sub_functions_sql, create_mantis_card_sql, create_mantis_plan_sql, create_mantis_milestone_sql,
    create_mantis_milestone_group_sql, create_mantis_operate_record_sql, create_mantis_mapping_rule_sql,
    create_mantis_share_record_sql, create_mantis_board_location_sql
)


def create_database_cnf(mode):
    db = {
        'tms': 'tms_db',
        'tms_dev': 'tms_db_dev',
        'tms_test': 'tms_db_test',
        'tm': 'tm_db',
        'tm_dev': 'tm_db_dev',
        'tm_test': 'tm_db_test',
        'ra': 'ra_db',
        'ra_dev': 'ra_db_dev',
        'ra_test': 'ra_db_test',
        'mantis': 'mantis_db_product_v2',
        'mantis_dev': 'mantis_db_dev',
        'mantis_test': 'mantis_db_test',
        'itc': 'itc_db',
        'itc_dev': 'itc_db_dev',
        'itc_test': 'itc_db_test',
        'tts': 'tts_db',
        'tts_dev': 'tts_db_dev',
        'tts_test': 'tts_db_test',
        'bmt': 'bmt_db',
        'bmt_dev': 'bmt_db_dev',
        'bmt_test': 'bmt_db_test',
    }
    database_cnf = {
        'host': '172.16.50.100',
        'port': 3306,
        'user': 'root',
        'password': 'Auditaee11..2021',
        'db': db.get(mode),
        'charset': 'utf8mb4'
    }
    return database_cnf


def create_connect(cnf, mode=None):
    conn = pymysql.connect(**cnf)
    if mode == 'dict':
        curr = conn.cursor(cursor=pymysql.cursors.DictCursor)
    else:
        curr = conn.cursor()
    return conn, curr


def create_tables(mode, sql_list):
    database = create_database_cnf(mode)
    conn, curr = create_connect(database)
    for item in sql_list:
        print(item)
        curr.execute(item)
    conn.commit()
    curr.close()
    conn.close()


def run(mode):
    sql_dict = {
        'bmt': [create_bmt_ticket_sql],
        'itc': [
            create_itc_wiki_entry_sql, create_itc_category_sql, create_itc_wiki_daily_browsing_record,
            create_itc_tag_sql
        ],
        'mantis': [
            create_mantis_board_sql, create_mantis_functions_sql, create_mantis_group_sql, create_mantis_card_group_sql,
            create_mantis_sw_map_sql, create_mantis_fuLi_sql, create_mantis_case_field_sql, create_mantis_test_case_sql,
            create_mantis_case_result_sql, create_mantis_fuLi_group_sql, create_mantis_filter_record_sql,
            create_mantis_sub_functions_sql, create_mantis_card_sql, create_mantis_plan_sql,
            create_mantis_milestone_sql, create_mantis_milestone_group_sql, create_mantis_operate_record_sql,
            create_mantis_mapping_rule_sql, create_mantis_share_record_sql, create_mantis_board_location_sql
        ],
        'ra': [
            create_ra_leave_sql, create_ra_draft_sql, create_ra_leave_type_sql
        ],
        'tm': [
            create_tm_ticket_sql, create_tm_time_consuming_sql,
            create_tm_scheduled_tasks_sql, create_tm_platform_sql
        ],
        'tms': [
            create_tms_user_sql, create_tms_role_sql, create_tms_project_sql, create_province_sql,
            create_city_sql, create_county_sql, create_tms_department_sql, create_tms_group_sql,
            create_tms_favorite_project_sql, create_tms_daily_activity_sql, create_tms_company_sql,
            create_tms_message_sql, create_tms_email_sql,  create_tms_schedule_email_sql,
            create_tms_schedule_history_sql,
        ],
        'tts': [create_tts_task_sql],
    }
    create_tables(mode, sql_dict.get(mode.split('_')[0]))


if __name__ == '__main__':
    """
    mode:  tms / tms_dev / tms_test | tm / tm_dev / tm_test | ra / ra_dev /ra_test | mantis / mantis_dev / mantis_test | 
           itc / itc_dev / itc_test | bmt / bmt_dev / bmt_test | tts / tts_dev / tts_test
    """

    # run('mantis_dev')
    # run('mantis_test')

    pass
