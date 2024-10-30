# -*- coding: utf-8 -*-
import base64
import json
import traceback
import jwt
from flask import request, session, Blueprint, make_response

from config.basic_setting import SECRET_KEY, SERVICE_MODE, LOGIN_FREE_VERIFICATION
from common_tools.status_code import response
from common_tools.tools import generate_md5, global_logger

middleware_blueprint = Blueprint('middleware', __name__)


# @middleware_blueprint.before_app_request
# def login_check():
#     if request.path in LOGIN_FREE_VERIFICATION:
#         return None
#     username = session.get('username')
#     user_key = session.get('user_key')
#     if SERVICE_MODE == 'develop':
#         if not user_key:
#             return None
#         else:
#             if generate_md5([username, SECRET_KEY]) != user_key:
#                 resp = response(300)
#                 return resp
#     elif SERVICE_MODE == 'product':
#         if not username or not user_key or generate_md5([username, SECRET_KEY]) != user_key:
#             resp = response(300)
#             return resp
#     return None


@middleware_blueprint.before_app_request
def login_check():
    request.user_info = {}
    if request.path in LOGIN_FREE_VERIFICATION:
        return None
    try:
        token = request.cookies.get('token')
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        if token and payload:
            request.user_info = payload
            return None
        else:
            resp = response(300)
            resp = make_response(resp)
            resp.delete_cookie('token')
            return resp
    except Exception as e:
        if SERVICE_MODE in ['develop', 'testing']:
            return None
        global_logger.error('traceback.format_exc():\n%s\n' % e)
        resp = response(300)
        resp = make_response(resp)
        resp.delete_cookie('token')
        return resp


@middleware_blueprint.after_app_request
def record_request(resp):
    global_logger.info(
        f'{request.remote_addr} -- {request.method} -- {request.path} -- {request.scheme}  -- {resp.status_code}'
    )
    return resp
