# -*- coding: utf-8 -*-

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from mantis.controller.mantis_test_cycle_tool import mantis_create_test_cycle_tool, mantis_edit_test_cycle_tool, \
    mantis_get_test_cycle_tool, mantis_delete_test_cycle_tool, mantis_get_test_cycle_insight_graph_tool
from mantis.mantis_status.status_code import response


test_cycle_blueprint = Blueprint('test_cycle_blueprint', __name__)


@swag_from('../mantis_swag_yaml/mantis_create_test_cycle.yml')
@test_cycle_blueprint.route('/mantis/create/test/cycle', methods=['POST'])
def mantis_create_test_cycle():
    func_dict = mantis_create_test_cycle_tool(request.json)
    resp = response(200, func_dict)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_edit_test_cycle.yml')
@test_cycle_blueprint.route('/mantis/edit/test/cycle', methods=['POST'])
def mantis_edit_test_cycle():
    func_dict = mantis_edit_test_cycle_tool(request.json)
    resp = response(200, func_dict)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_cycle.yml')
@test_cycle_blueprint.route('/mantis/get/test/cycle', methods=['GET'])
def mantis_get_test_cycle():
    func_dict = mantis_get_test_cycle_tool(request.json)
    resp = response(200, func_dict)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_delete_test_cycle.yml')
@test_cycle_blueprint.route('/mantis/delete/test/cycle', methods=['POST'])
def mantis_delete_test_cycle():
    func_dict = mantis_delete_test_cycle_tool(request.json)
    resp = response(200, func_dict)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_cycle_insight_graph.yml')
@test_cycle_blueprint.route('/mantis/delete/test/cycle', methods=['GET'])
def mantis_get_test_cycle_insight_graph():
    ret = mantis_get_test_cycle_insight_graph_tool(request.args)
    resp = response(200, ret)
    return jsonify(resp)
