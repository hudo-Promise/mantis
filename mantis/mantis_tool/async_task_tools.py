import traceback
import time
from concurrent.futures.thread import ThreadPoolExecutor
from common_tools.tools import global_logger
from functools import wraps
from flask import Flask
from mantis.models import init_db as mantis_init_db
from config.mantis_setting import instance_config as mantis_instance_config

service_app = Flask(__name__)

async_config_dict = {
    'mantis': mantis_instance_config
}


def decorator_app(project_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_message = func.__name__
            try:
                # start_time = time.time()
                # global_logger.info(f"start {log_message}")
                base_config = async_config_dict.get(project_name)
                base_config.SQLALCHEMY_ECHO = False
                service_app.config.from_object(base_config)
                mantis_init_db(service_app)
                with service_app.app_context():
                    result = func(*args, **kwargs)
                    # global_logger.info(f"{log_message} executed：%s" % (time.time() - start_time))
                    return result
            except:
                global_logger.error(f"{log_message} failed")
                global_logger.error('traceback.format_exc():\n%s\n' % traceback.format_exc())

        return wrapper

    return decorator


def async_task_new(project_name):
    def actual_decorator(func):
        decorator_app_func = decorator_app(project_name)(func)

        @wraps(decorator_app_func)
        def wrapper(*args, **kwargs):
            tms_execute = ThreadPoolExecutor(2)
            tms_execute.submit(decorator_app_func, *args, **kwargs)

        return wrapper

    return actual_decorator
