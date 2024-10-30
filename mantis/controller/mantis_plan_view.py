from flasgger import swag_from
from flask import Blueprint, jsonify, request

from mantis.controller.mantis_plan_tool import query_plan_tool, upload_plan_tool, insert_plan_to_database, \
    query_plan_info_tool
from mantis.mantis_status.status_code import response


mantis_plan_blueprint = Blueprint('plan', __name__)


@swag_from('../mantis_swag_yaml/mantis_upload_plan.yml')
@mantis_plan_blueprint.route('/mantis/upload/plan', methods=['POST'])
def mantis_upload_plan():
    result = upload_plan_tool(request)
    insert_plan_to_database(result)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_query_plan.yml')
@mantis_plan_blueprint.route('/mantis/query/plan', methods=['POST'])
def mantis_query_plan():
    result = query_plan_tool(request.json)
    resp = response(200, result)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_plan_info.yml')
@mantis_plan_blueprint.route('/mantis/plan/info', methods=['GET'])
def mantis_plan_info():
    result = query_plan_info_tool(request.args)
    resp = response(200, result)
    return jsonify(resp)