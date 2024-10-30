# -*- coding: utf-8 -*-
import json

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from common_tools.async_api_tool import update_mantis_graph
from common_tools.tools import op11_redis_client
from mantis.controller.mantis_milestone_tool import create_milestone, update_milestone, query_milestone, \
    delete_milestone_by_id, query_milestone_uuid_status
from mantis.mantis_status.status_code import response

milestone_blueprint = Blueprint('milestone', __name__)


@swag_from('../mantis_swag_yaml/add_milestone.yml')
@milestone_blueprint.route('/mantis/add/milestone', methods=['POST'])
def add_milestone():
    update_uuid, milestone_id = create_milestone(request.json)
    resp = response(200, {'update_uuid': update_uuid, 'milestone_id': milestone_id})
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/edit_milestone.yml')
@milestone_blueprint.route('/mantis/edit/milestone', methods=['POST'])
def edit_milestone():
    update_uuid = update_milestone(request.json)
    resp = response(200, {'update_uuid': update_uuid})
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/get_milestone.yml')
@milestone_blueprint.route('/mantis/get/milestone', methods=['GET'])
def get_milestone():
    data = query_milestone(request.args)
    resp = response(200, data)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/get_milestone_uuid.yml')
@milestone_blueprint.route('/mantis/get/uuid/status', methods=['GET'])
def get_milestone_uuid():
    data = query_milestone_uuid_status(request.args)
    if data.get('id'):
        resp = response(200, data)
    else:
        resp = response(10015)
    return jsonify(resp)
    pass


@swag_from('../mantis_swag_yaml/delete_milestone.yml')
@milestone_blueprint.route('/mantis/delete/milestone', methods=['POST'])
def delete_milestone():
    delete_milestone_by_id([request.json.get('milestone_id')])
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/milestone_test.yml')
@milestone_blueprint.route('/mantis/milestone/test', methods=['GET'])
def milestone_test():
    update_mantis_graph(29, 'personal')
    update_mantis_graph(29, 'all')
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/get_case_result_by_unique_id.yml')
@milestone_blueprint.route('/mantis/case/result', methods=['GET'])
def case_result_test():
    unique_id = request.args.get('unique_id')
    data = json.loads(op11_redis_client.get('case_result_data')).get(unique_id)
    resp = response(200, data=data)
    return jsonify(resp)
