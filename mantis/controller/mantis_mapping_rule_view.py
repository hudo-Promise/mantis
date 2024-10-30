# -*- coding: utf-8 -*-

from flasgger import swag_from
from flask import Blueprint, request

from mantis.controller.mantis_mapping_rule_tool import mantis_create_mapping_rule_tool, mantis_edit_mapping_rule_tool, \
    mantis_delete_mapping_rule_tool, mantis_get_mapping_rule_tool, mantis_clone_mapping_rule_tool, \
    mantis_check_mapping_name_tool
from mantis.mantis_status.status_code import response

mantis_mapping_rule_blueprint = Blueprint('mapping_rule', __name__)


@swag_from('../mantis_swag_yaml/mantis_create_mapping_rule.yml')
@mantis_mapping_rule_blueprint.route('/mantis/create/mapping/rule', methods=['POST'])
def mantis_create_mapping_rule():
    mantis_create_mapping_rule_tool(request.json)
    return response(200)


@swag_from('../mantis_swag_yaml/mantis_edit_mapping_rule.yml')
@mantis_mapping_rule_blueprint.route('/mantis/edit/mapping/rule', methods=['POST'])
def mantis_edit_mapping_rule():
    mantis_edit_mapping_rule_tool(request.json)
    return response(200)


@swag_from('../mantis_swag_yaml/mantis_delete_mapping_rule.yml')
@mantis_mapping_rule_blueprint.route('/mantis/delete/mapping/rule', methods=['POST'])
def mantis_delete_mapping_rule():
    mantis_delete_mapping_rule_tool(request.json)
    return response(200)


@swag_from('../mantis_swag_yaml/mantis_get_mapping_rule.yml')
@mantis_mapping_rule_blueprint.route('/mantis/get/mapping/rule', methods=['POST'])
def mantis_get_mapping_rule():
    result = mantis_get_mapping_rule_tool(request.json)
    return response(200, result)


@swag_from('../mantis_swag_yaml/mantis_clone_mapping_rule.yml')
@mantis_mapping_rule_blueprint.route('/mantis/clone/mapping/rule', methods=['POST'])
def mantis_clone_mapping_rule():
    result = mantis_clone_mapping_rule_tool(request.json)
    return response(200, result)


@swag_from('../mantis_swag_yaml/mantis_check_mapping_name.yml')
@mantis_mapping_rule_blueprint.route('/mantis/check/mapping/name', methods=['POST'])
def mantis_check_mapping_rule():
    result = mantis_check_mapping_name_tool(request.json)
    return response(200, result)
