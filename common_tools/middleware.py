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


@middleware_blueprint.after_app_request
def record_request(resp):
    global_logger.info(
        f'{request.remote_addr} -- {request.method} -- {request.path} -- {request.scheme}  -- {resp.status_code}'
    )
    return resp
