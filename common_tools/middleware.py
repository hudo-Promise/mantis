# -*- coding: utf-8 -*-
from flask import request, Blueprint
from common_tools.tools import global_logger
from common_tools.sso_handlers import login_check

middleware_blueprint = Blueprint('middleware', __name__)
middleware_blueprint.before_app_request(login_check)


@middleware_blueprint.after_app_request
def record_request(resp):
    global_logger.info(
        f'{request.remote_addr} -- {request.method} -- {request.path} -- {request.scheme}  -- {resp.status_code}'
    )
    return resp
