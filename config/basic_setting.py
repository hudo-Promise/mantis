import datetime
import logging
from config.rs_256_keys import RS_256_PUBLIC_KEY_DICT
import os

SERVICE_IP = '127.0.0.1'
LINK_URL = 'https://www.op-oneplatform.com'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_PATH = os.path.join(BASE_DIR, 'download_file')
LOG_PATH = os.path.join(BASE_DIR, 'logs')
SERVICE_MODE = 'develop'
VERSION = 'v1.0.0'
TIMEOUT = 48 * 3600
TOKEN_EXP = 12 * 3600
TOKEN_NAME = 'token'
TOKEN_MD5 = f'{TOKEN_NAME}_md5'
PASSWORD = 'Auditaee11..2021'
FORMAT_DATE = '%Y-%m-%d'
FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S'

HOST_DICT = {
    'product': '172.16.50.16',
    'develop': '172.16.50.100',
    'testing': '172.16.50.100'
}
HOST = HOST_DICT.get(SERVICE_MODE)

SECRET_KEY_DICT = {
    'product': 'audi--product--TPmi4aLWRbyVq8zu9v82dWYW1',
    'develop': 'audi--develop--TPmi4aLWRbyVq8zu9v82dWYW1',
    'testing': 'audi--testing--TPmi4aLWRbyVq8zu9v82dWYW1'
}
SECRET_KEY = SECRET_KEY_DICT.get(SERVICE_MODE)
PUBLIC_KEY = RS_256_PUBLIC_KEY_DICT.get(SERVICE_MODE)

SERVICE_PORT_DICT = {
    'product': 10051,
    'develop': 10052,
    'testing': 10053
}
SERVICE_PORT = SERVICE_PORT_DICT.get(SERVICE_MODE)

LOGIN_FREE_VERIFICATION = [
    '/v1.0.0/tms/user/login',
    '/v1.0.0/doc',
    '/v1.0.0/register',
    '/flasgger_static/swagger-ui.css',
    '/flasgger_static/swagger-ui-bundle.js',
    '/flasgger_static/swagger-ui-standalone-preset.js',
    '/flasgger_static/lib/jquery.min.js',
    '/apispecification.json',
    '/flasgger_static/favicon-32x32.png',
    '/v1.0.0/tms/create/message',
    '/v1.0.0/tms/create/email',
    '/v1.0.0/tms/user/invitation/check',
    '/v1.0.0/tms/user/invitation/register',
    '/v1.0.0/tms/user/code/send',
    '/v1.0.0/tms/user/code/check',
    '/v1.0.0/tms/user/password/reset',
    '/v1.0.0/info',
    '/v1.0.0/tms/get/remote/addr'
]

FREE_LOG_API_DICT = {
    'product': 'http://172.16.50.16:8210/freelog-api/create/log/record',
    'develop': 'http://172.16.50.100:8200/freelog-dev/create/log/record',
    'testing': 'http://172.16.50.100:8200/freelog-dev/create/log/record'
}
FREE_LOG_API = FREE_LOG_API_DICT.get(SERVICE_MODE)

NOT_LOG_PATH = [
    '/v1.0.0/doc',
    '/flasgger_static/swagger-ui.css',
    '/flasgger_static/swagger-ui-bundle.js',
    '/flasgger_static/swagger-ui-standalone-preset.js',
    '/flasgger_static/lib/jquery.min.js',
    '/flasgger_static/swagger-ui.css.map',
    '/flasgger_static/favicon-32x32.png',
    '/apispecification.json',
]

KPM_HCP3_PERF_API_DICT = {
    'product': 'http://172.16.50.3:9528/kpm-api/api/perf/upload/',
    'develop': 'http://172.16.51.2:8089/kpm-api-test/api/perf/upload/',
    'testing': 'http://172.16.51.2:8089/kpm-api-test/api/perf/upload/'
}
KPM_HCP3_PERF_API = KPM_HCP3_PERF_API_DICT.get(SERVICE_MODE)

db_dict = {
    'mantis': 'mantis_db',
}

mysql_port_dict = {
    'product': 33061,
    'develop': 33062,
    'testing': 33063
}
MYSQL_PORT = mysql_port_dict.get(SERVICE_MODE)


def mysql_config(mysql_type):
    config = {
        'host': HOST,
        'port': MYSQL_PORT,
        'user': 'root',
        'password': PASSWORD,
        'db': db_dict.get(mysql_type),
        'charset': 'utf8'
    }
    return config


redis_port_dict = {
    'product': 63791,
    'develop': 63792,
    'testing': 63793
}
REDIS_PORT = redis_port_dict.get(SERVICE_MODE)

redis_config = {
    'host': HOST,
    'port': REDIS_PORT,
    'db': 0,
    'password': PASSWORD,
    'decode_responses': True,
    'max_connections': 100
}

redis_blacklist_config = {
    'host': HOST,
    'port': REDIS_PORT,
    'db': 1,
    'password': PASSWORD,
    'decode_responses': True,
    'max_connections': 100
}

# AOS CONFIG
AOS_SERVICE_PORT_DICT = {
    'product': 10011,
    'develop': 10012,
    'testing': 10013,
}

AOS_API_DICT = {
    'product': '/aos-api',
    'develop': '/aos-dev',
    'testing': '/aos-test'
}

AOS_PREFIX = 'http://172.16.50.11'
BASE_URL = f'{AOS_PREFIX}:{AOS_SERVICE_PORT_DICT.get(SERVICE_MODE)}{AOS_API_DICT.get(SERVICE_MODE)}/{VERSION}/'


class BaseConfig(object):
    SECRET_KEY = "TPmi4aLWRbyVq8zu9v82dWYW1"
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True
    # 数据库连接池的大小
    SQLALCHEMY_POOL_SIZE = 10
    # 指定数据库连接池的超时时间
    SQLALCHEMY_POOL_TIMEOUT = 10
    # 控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃。
    SQLALCHEMY_MAX_OVERFLOW = 2
    LOG_LEVEL = logging.DEBUG
    JSON_AS_ASCII = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=12)
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'


class InstanceConfig(BaseConfig):
    def __init__(self, db):
        self.SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{PASSWORD}@{HOST}:{MYSQL_PORT}/{db}?charset=utf8mb4"

    @classmethod
    def swagger_config(cls, base_path):
        return {
            "headers": [],
            "specs": [
                {
                    "endpoint": 'apispec_2',
                    "route": f'{base_path}/apispecification.json',
                }
            ],
            "static_url_path": f'{base_path}/flasgger_static',
            "swagger_ui": True,
            "specs_route": f"{base_path}/v1.0.0/doc",
            # "basePath": base_path
        }

    @classmethod
    def template_config(cls, title):
        return {
            "info": {
                "title": f"{title} SYSTEM API",
                "description": f"{title} SYSTEM",
                "version": VERSION
            }
        }
