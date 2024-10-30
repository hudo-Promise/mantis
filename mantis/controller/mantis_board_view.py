# -*- coding: utf-8 -*-

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from mantis.controller.mantis_board_tool import create_board, delete_board_func, get_board_func, get_board_data_func, \
    create_board_location_func, update_board_location_func, edit_board_tool, clone_dashboard_tool
from mantis.mantis_status.status_code import response


board_blueprint = Blueprint('board', __name__)


@swag_from('../mantis_swag_yaml/add_board.yml')
@board_blueprint.route('/mantis/add/board', methods=['POST'])
def add_board():
    code, _ = create_board(request.json)
    resp = response(code)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/edit_board.yml')
@board_blueprint.route('/mantis/edit/board', methods=['POST'])
def edit_board():
    code = edit_board_tool(request.json)
    resp = response(code)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/delete_board.yml')
@board_blueprint.route('/mantis/delete/board', methods=['POST'])
def delete_board():
    code = delete_board_func(request.json)
    resp = response(code)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/get_board.yml')
@board_blueprint.route('/mantis/get/board', methods=['POST'])
def get_board():
    data = get_board_func(request.json)
    resp = response(200, data)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/create_board_location.yml')
@board_blueprint.route('/mantis/create/board/location', methods=['POST'])
def create_board_location():
    create_board_location_func(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/update_board_location.yml')
@board_blueprint.route('/mantis/update/board/location', methods=['POST'])
def update_board_location():
    update_board_location_func(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/get_board_data.yml')
@board_blueprint.route('/mantis/get/board/data', methods=['GET'])
def get_board_data():
    data = get_board_data_func(request.args)
    resp = response(200, data)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mantis_clone_dashboard.yml')
@board_blueprint.route('/mantis/clone/dashboard', methods=['POST'])
def mantis_clone_dashboard():
    clone_dashboard_tool(request.json)
    resp = response(200)
    return jsonify(resp)
