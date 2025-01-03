# -*- coding: utf-8 -*-

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from mantis.mantis_status.status_code import response
from mantis.controller.mantis_function_tool import query_functions, mantis_create_functions_tool, \
    mantis_edit_functions_tool, mantis_delete_functions_tool, mantis_create_field_value_tool, \
    mantis_edit_field_value_tool, mantis_delete_field_value_tool, mantis_check_field_value_tool, mantis_check_fuli_used

function_blueprint = Blueprint('function', __name__)


@swag_from('../mantis_swag_yaml/functions.yml')
@function_blueprint.route('/mantis/functions', methods=['GET'])
def functions():
    func_dict = query_functions()
    resp = response(200, func_dict)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_create_functions.yml')
@function_blueprint.route('/mantis/create/functions', methods=['POST'])
def mantis_create_functions():
    new_id = mantis_create_functions_tool(request.json)
    resp = response(200, new_id)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_edit_functions.yml')
@function_blueprint.route('/mantis/edit/functions', methods=['POST'])
def mantis_edit_functions():
    mantis_edit_functions_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_delete_functions.yml')
@function_blueprint.route('/mantis/delete/functions', methods=['POST'])
def mantis_delete_functions():
    mantis_delete_functions_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_create_field_value.yml')
@function_blueprint.route('/mantis/create/field/value', methods=['POST'])
def mantis_create_field_value():
    mantis_create_field_value_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_edit_field_value.yml')
@function_blueprint.route('/mantis/edit/field/value', methods=['POST'])
def mantis_edit_field_value():
    mantis_edit_field_value_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_delete_field_value.yml')
@function_blueprint.route('/mantis/delete/field/value', methods=['POST'])
def mantis_delete_field_value():
    mantis_delete_field_value_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_check_field_value.yml')
@function_blueprint.route('/mantis/check/field/value', methods=['POST'])
def mantis_check_field_value():
    result = mantis_check_field_value_tool(request.json)
    resp = response(200, result)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_check_fuli_used.yml')
@function_blueprint.route('/mantis/check/fuli/used', methods=['GET'])
def mantis_check_field_value():
    ret = mantis_check_fuli_used(request.args)
    resp = response(200, ret)
    return jsonify(resp)