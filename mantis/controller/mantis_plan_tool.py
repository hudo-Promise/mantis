import json

import xlrd

from common_tools.tools import create_current_format_time, generate_uuid, global_logger
from mantis.controller.mantis_case_tool import get_case_func
from mantis.models import mantis_db
from mantis.models.mantis_plan import MantisPlan


def upload_plan_tool(request_param):
    file = request_param.files.get('files')
    content = file.read()
    data = xlrd.open_workbook(file_contents=content)
    table_data = data.sheet_by_index(0)
    rows = table_data.nrows
    cols = table_data.ncols
    plan_data = []
    for row in range(1, rows):
        create_time = create_current_format_time()
        value_list = table_data.row_values(rowx=row, start_colx=0, end_colx=cols)
        row_dict = {
            'unique_id': generate_uuid(),
            'name': value_list[0],
            'description': value_list[1],
            'creator': value_list[2],
            'project': json.loads(value_list[3]),
            'function': json.loads(value_list[4]),
            'sub_function': json.loads(value_list[5]),
            'market': json.loads(value_list[6]),
            'language': json.loads(value_list[7]),
            'cluster': value_list[8],
            'platform': json.loads(value_list[9]),
            'level': json.loads(value_list[10]),
            'carline': json.loads(value_list[11]),
            'case_list': json.loads(value_list[12]),
            'create_time': create_time,
            'update_time': create_time,
            'delete_flag': 0
        }
        plan_data.append(row_dict)
    return plan_data


def insert_plan_to_database(plan_data):
    mantis_db.session.execute(MantisPlan.__table__.insert(), plan_data)
    mantis_db.session.commit()


def query_plan_tool(request_params):
    page_num = request_params.get('page_num')
    page_size = request_params.get('page_size')
    plans = MantisPlan.query.filter().limit(int(page_size)).offset((int(page_num) - 1) * int(page_size)).all()
    plan_list = list(map(generate_plan_dict, plans))
    return plan_list


def generate_plan_dict(plan):
    plan_dict = {
        'id': plan.id,
        'uuid': plan.unique_id,
        'name': plan.name,
        'description': plan.description,
        'creator': plan.creator,
        'project': plan.project,
        'function': plan.function,
        'sub_function': plan.sub_function,
        'market': plan.market,
        'language': plan.language,
        'cluster': plan.cluster,
        'level': plan.level,
        'platform': plan.platform,
        'carline': plan.carline,
        'case_list': plan.case_list,
        'create_time': str(plan.create_time),
        'update_time': str(plan.update_time),
        'delete_flag': plan.delete_flag
    }
    return plan_dict


def query_plan_info_tool(request_params):
    unique_id = request_params.get('uuid')
    plan = MantisPlan.query.filter(MantisPlan.unique_id == unique_id).first()
    filter_dict = {
        'case_id': plan.case_list if plan else [0],
        'page_size': int(request_params.get('page_size')),
        'page_num': int(request_params.get('page_num'))
    }
    data, total_num = get_case_func(filter_dict)
    result = {
        'data': data,
        'total_num': total_num
    }
    return result
