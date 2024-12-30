from flasgger import swag_from
from flask import Blueprint, jsonify, request

from mantis.controller.mantis_project_tool import mantis_create_project_tool, mantis_edit_project_tool, \
    mantis_delete_project_tool, mantis_get_project_tool
from mantis.mantis_status.status_code import response


mantis_project_blueprint = Blueprint('mantis_project', __name__)


@swag_from('../mantis_swag_yaml/mantis_create_project.yml')
@mantis_project_blueprint.route('/mantis/create/project', methods=['POST'])
def mantis_create_project():
    mantis_create_project_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_edit_project.yml')
@mantis_project_blueprint.route('/mantis/edit/project', methods=['POST'])
def mantis_edit_project():
    mantis_edit_project_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_delete_project.yml')
@mantis_project_blueprint.route('/mantis/delete/project', methods=['POST'])
def mantis_delete_project():
    mantis_delete_project_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_get_project.yml')
@mantis_project_blueprint.route('/mantis/get/project', methods=['GET'])
def mantis_get_project():
    ret = mantis_get_project_tool(request.json)
    resp = response(200, ret)
    return jsonify(resp)
