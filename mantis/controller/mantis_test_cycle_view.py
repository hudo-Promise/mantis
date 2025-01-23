# -*- coding: utf-8 -*-

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from mantis.controller.mantis_test_cycle_tool import mantis_create_test_cycle_tool, mantis_edit_test_cycle_tool, \
    mantis_get_test_cycle_tool, mantis_delete_test_cycle_tool, mantis_get_test_cycle_insight_graph_tool, \
    mantis_get_test_cycle_burnout_diagram_tool, mantis_get_test_cycle_pie_chart_tool, \
    mantis_test_cycle_work_report_tool, mantis_get_test_cycle_by_milestone_tool, mantis_get_test_cycle_group_info_tool, \
    mantis_get_test_case_by_test_cycle_tool, mantis_create_cycle_draft_cache, mantis_get_cycle_draft_cache, \
    mantis_delete_cycle_draft_cache
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
@test_cycle_blueprint.route('/mantis/get/test/cycle', methods=['POST'])
def mantis_get_test_cycle():
    func_dict = mantis_get_test_cycle_tool(request.json)
    resp = response(200, func_dict)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_cycle_by_milestone.yml')
@test_cycle_blueprint.route('/mantis/get/test/cycle/by/milestone', methods=['GET'])
def mantis_get_test_cycle_by_milestone():
    ret = mantis_get_test_cycle_by_milestone_tool(request.args)
    resp = response(200, ret)
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


@swag_from('../mantis_swag_yaml/mantis_get_test_cycle_group_info.yml')
@test_cycle_blueprint.route('/mantis/get/test/cycle/group/info', methods=['GET'])
def mantis_get_test_cycle_group_info():
    ret = mantis_get_test_cycle_group_info_tool()
    resp = response(200, ret)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_test_case_by_cycle.yml')
@test_cycle_blueprint.route('/mantis/get/test/case/by/cycle', methods=['GET'])
def mantis_get_test_case_by_test_cycle():
    ret = mantis_get_test_case_by_test_cycle_tool(request.args)
    resp = response(200, ret)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_create_cycle_draft.yml')
@test_cycle_blueprint.route('/mantis/create/cycle/draft', methods=['POST'])
def mantis_create_cycle_draft():
    code = mantis_create_cycle_draft_cache(request.json)
    resp = response(code)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_cycle_draft.yml')
@test_cycle_blueprint.route('/mantis/get/cycle/draft', methods=['GET'])
def mantis_get_cycle_draft():
    data = mantis_get_cycle_draft_cache(request.args)
    resp = response(200, data)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_delete_cycle_draft.yml')
@test_cycle_blueprint.route('/mantis/delete/cycle/draft', methods=['POST'])
def mantis_delete_cycle_draft():
    mantis_delete_cycle_draft_cache(request.json)
    resp = response(200)
    return jsonify(resp)
