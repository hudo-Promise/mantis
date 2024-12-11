import jwt
import redis
from flask import request, make_response
from config.basic_setting import SECRET_KEY, SERVICE_MODE, LOGIN_FREE_VERIFICATION, redis_blacklist_config, PUBLIC_KEY, \
    TOKEN_NAME, TOKEN_MD5
from common_tools.status_code import response
from common_tools.tools import global_logger
from config.mantis_setting import MANTIS_API as API_PREFIX


def activate_blacklist_redis_client():
    redis_client = redis.StrictRedis(**redis_blacklist_config)
    return redis_client


blacklist_redis_client = activate_blacklist_redis_client()


def set_not_login():
    """验证失败后清除token并返回"""
    resp = response(300)
    resp = make_response(resp)
    resp.delete_cookie(TOKEN_NAME)
    resp.delete_cookie(TOKEN_MD5)
    return resp


def is_blacklisted(token_md5):
    """
    判断某个值是否在黑名单中
    :param token_md5: 要查询的值
    :return: 布尔值，True 表示在黑名单中，False 表示不在
    """
    return blacklist_redis_client.exists(token_md5) == 1


def login_check():
    request.user_info = {}
    url_path = request.path.replace(API_PREFIX, '', 1)
    if url_path in LOGIN_FREE_VERIFICATION:
        return None
    try:
        token = request.cookies.get(TOKEN_NAME)
        token_md5 = request.cookies.get(TOKEN_MD5, '')
        # payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'])
        # 判断当前token是否加入了黑名单
        if not is_blacklisted(token_md5) and token and payload:
            request.user_info = payload
            return None
        else:
            return set_not_login()
    except Exception as e:
        if (SERVICE_MODE in ['develop', 'testing']
                and 'www.op-oneplatform.com' not in
                request.headers.get('Origin', request.headers.get('Referer', ''))):
            return None
        global_logger.error('traceback.format_exc():\n%s\n' % e)
        return set_not_login()
