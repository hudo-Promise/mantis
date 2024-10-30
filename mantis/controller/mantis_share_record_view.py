# -*- coding: utf-8 -*-
import json

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from mantis.controller.mantis_share_record_tool import create_share_record_tool, mark_station_mail_tool, \
    delete_station_mail_tool, query_station_mail_tool, query_share_detail_by_url, batch_query_public_detail
from mantis.mantis_status.status_code import response

share_record_blueprint = Blueprint('share_record', __name__)


@swag_from('../mantis_swag_yaml/create_share_record.yml')
@share_record_blueprint.route('/mantis/create/share/record', methods=['POST'])
def create_share_record():
    code, result = create_share_record_tool(request.json)
    resp = response(code, result)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/mark_station_mail.yml')
@share_record_blueprint.route('/mantis/mark/station/mail', methods=['POST'])
def mark_station_mail():
    mark_station_mail_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/delete_station_mail.yml')
@share_record_blueprint.route('/mantis/delete/station/mail', methods=['POST'])
def handle_share_record():
    delete_station_mail_tool(request.json)
    resp = response(200)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/query_station_mail.yml')
@share_record_blueprint.route('/mantis/query/station/mail', methods=['POST'])
def query_station_mail():
    result = query_station_mail_tool(request.json)
    resp = response(200, result)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/query_share_detail.yml')
@share_record_blueprint.route('/mantis/query/share/detail', methods=['GET'])
def query_share_detail():
    code, result = query_share_detail_by_url(request.args)
    resp = response(code, result)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/query_public_detail.yml')
@share_record_blueprint.route('/mantis/query/public/detail', methods=['POST'])
def query_public_detail():
    code, result = batch_query_public_detail(request.json)
    resp = response(code, result)
    return jsonify(resp)
