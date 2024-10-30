# -*- coding: utf-8 -*-
import time

from flasgger import swag_from
from flask import Blueprint, jsonify, request, Response

from common_tools.async_api_tool import update_mantis_graph
from mantis.controller.mantis_case_tool import get_digital_map_case_func, edit_case_func, create_case_func, \
    update_digital_map_case_func, delete_case_func, get_case_func, download_file, upload_file_func, \
    mantis_create_filter_config_tool, mantis_edit_filter_config_tool, mantis_delete_filter_config_tool, \
    mantis_get_filter_config_tool, get_case_result_tool, mantis_get_sw_tool, mantis_generate_case_format_string_tool, \
    edit_case_result_func, create_case_result_func
from mantis.mantis_status.status_code import response

case_blueprint = Blueprint('case', __name__)


@swag_from('../mantis_swag_yaml/upload.yml')
@case_blueprint.route('/mantis/upload', methods=['POST'])
def upload():
    result = upload_file_func(request)
    resp = response(result.get('code'), result.get('data'))
    if result.get('msg'):
        resp['msg'] = result.get('msg')
    return resp


@swag_from('../mantis_swag_yaml/download.yml')
@case_blueprint.route('/mantis/download', methods=['POST'])
def download():
    filename, results = download_file(request.json)
    resp_stream = Response(
        results,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            "Content-Disposition": 'attachment; filename=%s.xls' % filename,
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )
    return resp_stream


@swag_from('../mantis_swag_yaml/get_case.yml')
@case_blueprint.route('/mantis/get/case', methods=['POST'])
def get_case():
    data, total_num = get_case_func(request.json)
    try:
        resp = response(200, data)
        resp['total_num'] = total_num
        return jsonify(resp)
    except Exception as e:
        print(e)
        resp = response(404)
        return jsonify(resp)


@swag_from('../mantis_swag_yaml/create_case.yml')
@case_blueprint.route('/mantis/create/case', methods=['POST'])
def create_case():
    code, test_case_id = create_case_func(request.json)
    if code == 200:
        update_mantis_graph(request.json.get('userid'), 'personal')
    resp = response(code, {'test_case_id': test_case_id})
    return resp


@swag_from('../mantis_swag_yaml/edit_case.yml')
@case_blueprint.route('/mantis/edit/case', methods=['POST'])
def edit_case():
    code = edit_case_func(request.json)
    if code == 200:
        update_mantis_graph(request.json.get('userid'), 'personal')
    resp = response(code)
    return resp


@swag_from('../mantis_swag_yaml/delete_case.yml')
@case_blueprint.route('/mantis/delete/case', methods=['POST'])
def delete_case():
    code = delete_case_func(request.json)
    if code == 200:
        update_mantis_graph(request.json.get('userid'), 'personal')
    resp = response(code)
    return resp


@swag_from('../mantis_swag_yaml/update_digital_map_case.yml')
@case_blueprint.route('/mantis/update/digital/map/case', methods=['POST'])
def update_digital_map_case():
    update_digital_map_case_func(request.json)
    resp = response(200)
    return resp


@swag_from('../mantis_swag_yaml/get_digital_map_case.yml')
@case_blueprint.route('/mantis/get/digital/map/case', methods=['GET'])
def get_digital_map_case():
    # 查询case
    result = get_digital_map_case_func()
    resp = response(200, result)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_create_filter_config.yml')
@case_blueprint.route('/mantis/create/filter/config', methods=['POST'])
def mantis_create_filter_config():
    mantis_create_filter_config_tool(request.json)
    return response(200)


@swag_from('../mantis_swag_yaml/mantis_edit_filter_config.yml')
@case_blueprint.route('/mantis/edit/filter/config', methods=['POST'])
def mantis_edit_filter_config():
    mantis_edit_filter_config_tool(request.json)
    return response(200)


@swag_from('../mantis_swag_yaml/mantis_delete_filter_config.yml')
@case_blueprint.route('/mantis/delete/filter/config', methods=['POST'])
def mantis_delete_filter_config():
    mantis_delete_filter_config_tool(request.json)
    return response(200)


@swag_from('../mantis_swag_yaml/mantis_get_filter_config.yml')
@case_blueprint.route('/mantis/get/filter/config', methods=['POST'])
def mantis_get_filter_config():
    ret = mantis_get_filter_config_tool(request.json)
    return response(200, ret)


@swag_from('../mantis_swag_yaml/mantis_get_case_result.yml')
@case_blueprint.route('/mantis/get/case/result', methods=['POST'])
def mantis_get_case_result():
    ret = get_case_result_tool(request.json)
    return response(200, ret)


@swag_from('../mantis_swag_yaml/mantis_get_sw.yml')
@case_blueprint.route('/mantis/get/sw/', methods=['GET'])
def mantis_get_sw():
    ret = mantis_get_sw_tool()
    return response(200, ret)


@swag_from('../mantis_swag_yaml/mantis_generate_case_format_string.yml')
@case_blueprint.route('/mantis/generate/case/format/string', methods=['GET'])
def mantis_generate_case_format_string():
    ret = mantis_generate_case_format_string_tool(request.args)
    return response(200, ret)


@swag_from('../mantis_swag_yaml/mantis_create_case_result.yml')
@case_blueprint.route('/mantis/create/case/result', methods=['POST'])
def mantis_create_case_result():
    create_case_result_func(request.json)
    return response(200)


@swag_from('../mantis_swag_yaml/mantis_edit_case_result.yml')
@case_blueprint.route('/mantis/edit/case/result', methods=['POST'])
def mantis_edit_case_result():
    edit_case_result_func(request.json)
    return response(200)
