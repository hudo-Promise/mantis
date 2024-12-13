# -*- coding: utf-8 -*-

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from mantis.controller.mantis_test_cycle_tool import mantis_create_test_cycle_tool, mantis_edit_test_cycle_tool, \
    mantis_get_test_cycle_tool, mantis_delete_test_cycle_tool, mantis_get_test_cycle_insight_graph_tool, \
    mantis_get_test_cycle_burnout_diagram_tool, mantis_get_test_cycle_pie_chart_tool, mantis_test_cycle_work_report_tool
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
@test_cycle_blueprint.route('/mantis/get/test/cycle/insight/graph', methods=['GET'])
def mantis_get_test_cycle_insight_graph():
    ret = mantis_get_test_cycle_insight_graph_tool(request.args)
    resp = response(200, ret)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_cycle_burnout_diagram.yml')
@test_cycle_blueprint.route('/mantis/get/test/cycle/burnout/diagram', methods=['GET'])
def mantis_get_test_cycle_burnout_diagram():
    ret = mantis_get_test_cycle_burnout_diagram_tool(request.args)
    resp = response(200, ret)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_cycle_pie_chart.yml')
@test_cycle_blueprint.route('/mantis/get/test/cycle/pie/chart', methods=['GET'])
def mantis_get_test_cycle_pie_chart():
    ret = mantis_get_test_cycle_pie_chart_tool(request.args)
    resp = response(200, ret)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_cycle_work_report.yml')
@test_cycle_blueprint.route('/mantis/get/test/cycle/work_report', methods=['GET'])
def mantis_test_cycle_work_report():
    ret = mantis_test_cycle_work_report_tool()
    resp = response(200, ret)
    return jsonify(resp)
