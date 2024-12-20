from flask import request, Blueprint
from common_tools.tools import global_logger
from common_tools.status_code import response
from config.basic_setting import SERVICE_MODE, FREE_LOG_API, NOT_LOG_PATH
from config.mantis_setting import MANTIS_API as API_PREFIX
from common_tools.tools import async_task
import datetime
import json
import traceback
import requests

free_log_middleware_blueprint = Blueprint('free_log_middleware', __name__)


def get_log_data(request, resp):
    try:
        log_time = str(datetime.datetime.now())
        try:
            request_body = dict(request.json) if request.method == 'POST' else dict(request.args)
        except:
            request_body = {}
        try:
            response_body = resp.get_data(as_text=True)
            response_body_dict = json.loads(response_body) if response_body else {}
        except:
            response_body_dict = {}
        if hasattr(request, 'error_message'):
            error_message = request.error_message
            log_level = 'ERROR'
        else:
            error_message = ''
            log_level = 'INFO'
        data = {
            "service": "mantis",
            "env": SERVICE_MODE,
            "log_source": "backend",
            "log_type": "HTTP",
            "request_path": request.path,
            "request_method": request.method,
            "method_name": request.endpoint,
            "log_level": log_level,
            "log_time": log_time,
            "error_message": error_message,
            "additional_data": {
                "status_code": resp.status_code,
                "request_body": request_body,
                "response_body": response_body_dict,
            }
        }
        return data
    except:
        return {}


@async_task
def async_send_free_log(log_data):
    try:
        requests.post(FREE_LOG_API, json=log_data, timeout=10)
    except:
        global_logger.error(traceback.format_exc())


def handle_generic_exception(e):
    """添加全局异常日志"""
    error_message = traceback.format_exc()
    request.error_message = error_message
    global_logger.error(error_message)
    return response(500)


@free_log_middleware_blueprint.after_app_request
def record_request(resp):
    try:
        url_path = request.path.replace(API_PREFIX, '', 1)
        if url_path not in NOT_LOG_PATH:
            log_data = get_log_data(request, resp)
            async_send_free_log(log_data)
    except:
        global_logger.error(traceback.format_exc())
    return resp


def init_free_log(app):
    app.register_error_handler(Exception, handle_generic_exception)
    app.register_blueprint(free_log_middleware_blueprint)
