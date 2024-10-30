# -*- coding: utf-8 -*-

import xlrd
from flask import request, Blueprint, session

from common_tools.tools import create_current_format_time
from mantis.mantis_status import user_operate_record_url_list
from mantis.models import mantis_db
from mantis.models.mantis_share_record import MantisOperateRecord
from common_tools.tools import global_logger

mantis_middleware_blueprint = Blueprint('mantis_middleware', __name__)


@mantis_middleware_blueprint.before_app_request
def record_user_operate():
    if request.method == 'OPTIONS':
        return None
    url_path = request.path
    if url_path not in user_operate_record_url_list:
        return None

    if url_path == '/v1.0.0/mantis/upload':
        operate_content = parse_upload_params()
    else:
        operate_content = request.json
    operate_record_dict = {
        # 'operator': session.get('userinfo', {}).get('id'),
        # 'operator_name': session.get('userinfo', {}).get('username'),
        'operator': request.user_info.get('id'),
        'operator_name': request.user_info.get('username'),
        'operate_url': url_path,
        'operate_content': operate_content,
        'operate_time': create_current_format_time()
    }
    insert_operate_record(operate_record_dict)
    return None


def insert_operate_record(operate_record_dict):
    mantis_db.session.execute(MantisOperateRecord.__table__.insert(), operate_record_dict)
    mantis_db.session.commit()


def parse_upload_params():
    operate_content = {'mode': request.form.get('mode'), 'case_info': []}
    file = request.files
    content = file.get('files').read()
    data = xlrd.open_workbook(file_contents=content)
    table = data.sheet_by_index(0)
    rows = table.nrows
    for row in range(1, rows):
        m_id = table.cell(row, 0).value
        operate_content['case_info'].append(m_id)
    request.files.get('files').seek(0)
    return operate_content
