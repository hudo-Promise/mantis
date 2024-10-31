# -*- coding: utf-8 -*-
import json

from flasgger import swag_from
from flask import Blueprint, jsonify, request, session

from common_tools.tools import generate_week, create_current_format_time
from mantis.controller.mantis_common_tool import get_common_info_tool, sw_map_tool
from mantis.mantis_status.status_code import response

mantis_common_blueprint = Blueprint('mantis_common', __name__)


@swag_from('../mantis_swag_yaml/get_current_week.yml')
@mantis_common_blueprint.route('/mantis/get/current/week', methods=['GET'])
def get_current_week():
    week = generate_week()
    year = create_current_format_time()[:4]
    resp = response(200, {'year': year, "week": week})
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/get_common_info.yml')
@mantis_common_blueprint.route('/mantis/get/common/info', methods=['GET'])
def get_common_info():
    common_info = get_common_info_tool()
    resp = response(200, common_info)
    return jsonify(resp)


@swag_from('../mantis_swag_yaml/operate_sw_map.yml')
@mantis_common_blueprint.route('/mantis/operate/sw/map', methods=['POST'])
def operate_sw_map():
    sw_map_tool(request.json)
    resp = response(200)
    return jsonify(resp)
