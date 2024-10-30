# -*- coding: utf-8 -*-

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from mantis.controller.mantis_card_tool import create_card_func, parse_edit_card_params, edit_card_func, \
    delete_card_func, query_card_func
from mantis.mantis_status.status_code import response

card_blueprint = Blueprint('card', __name__)


@swag_from('../mantis_swag_yaml/create_card.yml')
@card_blueprint.route('/mantis/create/card', methods=['POST'])
def create_card():
    update_uuid, card_id = create_card_func(request.json)
    resp = response(200, {'update_uuid': update_uuid, 'card_id': card_id})
    return resp


@swag_from('../mantis_swag_yaml/edit_card.yml')
@card_blueprint.route('/mantis/edit/card', methods=['POST'])
def edit_card():
    board_id, card_id, update_dict = parse_edit_card_params(request.json)
    update_uuid = edit_card_func(board_id, card_id, update_dict)
    resp = response(200, {'update_uuid': update_uuid})
    return resp


@swag_from('../mantis_swag_yaml/delete_card.yml')
@card_blueprint.route('/mantis/delete/card', methods=['POST'])
def delete_card():
    delete_card_func([request.json.get('card_id')])
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/get_card.yml')
@card_blueprint.route('/mantis/get/card', methods=['GET'])
def get_card():
    data = query_card_func(request.args)
    resp = response(200, data)
    return jsonify(resp)
