from application import app
from werkzeug.serving import run_simple
from config.basic_setting import SERVICE_IP, SERVICE_PORT


if __name__ == "__main__":
    run_simple(SERVICE_IP, SERVICE_PORT, app, threaded=True)


"""
用于本地启动
"""