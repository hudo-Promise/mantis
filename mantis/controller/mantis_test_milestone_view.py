# -*- coding: utf-8 -*-

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from mantis.controller.mantis_test_milestone_tool import mantis_create_test_milestone_tool, \
    mantis_edit_test_milestone_tool, mantis_get_test_milestone_tool, mantis_delete_test_milestone_tool, \
    get_test_milestone_insight_graph_tool, get_test_milestone_group_graph_tool, mantis_test_milestone_group_order_tool, \
    mantis_get_test_milestone_time_table_tool
from mantis.mantis_status.status_code import response


test_milestone_blueprint = Blueprint('test_milestone_blueprint', __name__)


@swag_from('../mantis_swag_yaml/mantis_create_test_milestone.yml')
@test_milestone_blueprint.route('/mantis/create/test/milestone', methods=['POST'])
def mantis_create_test_milestone():
    mantis_create_test_milestone_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_edit_test_milestone.yml')
@test_milestone_blueprint.route('/mantis/edit/test/milestone', methods=['POST'])
def mantis_edit_test_milestone():
    mantis_edit_test_milestone_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_milestone.yml')
@test_milestone_blueprint.route('/mantis/get/test/milestone', methods=['GET'])
def mantis_get_test_milestone():
    ret = mantis_get_test_milestone_tool(request.args)
    resp = response(200, ret)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_delete_test_milestone.yml')
@test_milestone_blueprint.route('/mantis/delete/test/milestone', methods=['POST'])
def mantis_get_delete_milestone():
    ret = mantis_delete_test_milestone_tool(request.json)
    resp = response(200, ret)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_milestone_insight_graph.yml')
@test_milestone_blueprint.route('/mantis/get/test/milestone/insight/graph', methods=['GET'])
def mantis_get_test_milestone_insight_graph():
    ret = get_test_milestone_insight_graph_tool(request.args)
    resp = response(200, ret)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_milestone_group_graph.yml')
@test_milestone_blueprint.route('/mantis/get/test/milestone/group/graph', methods=['GET'])
def mantis_get_test_milestone_group_graph():
    ret = get_test_milestone_group_graph_tool(request.args)
    resp = response(200, ret)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_milestone_group_order.yml')
@test_milestone_blueprint.route('/mantis/get/test/milestone/group/order', methods=['GET'])
def mantis_get_test_milestone_group_order():
    ret = mantis_test_milestone_group_order_tool(request.args)
    resp = response(200, ret)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_milestone_time_table.yml')
@test_milestone_blueprint.route('/mantis/get/test/milestone/time/table', methods=['GET'])
def mantis_get_test_milestone_time_table():
    ret = mantis_get_test_milestone_time_table_tool()
    resp = response(200, ret)
    return jsonify(resp)
