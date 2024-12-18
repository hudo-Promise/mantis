import calendar
import datetime
import hashlib
import time
import uuid
from concurrent.futures.thread import ThreadPoolExecutor
from functools import wraps
from dateutil.relativedelta import relativedelta
import pymysql
import redis

from common_tools.logger import InitLog
from config.basic_setting import redis_config, FORMAT_DATE, FORMAT_DATETIME


def create_current_format_time():
    return time.strftime(FORMAT_DATETIME, time.localtime())


def get_gap_days(base_date, cur_date, format=FORMAT_DATETIME, count_type='days'):
    """
    获取当前日期与计算日期时间间隔
    :param base_date: 起始日期
    :param cur_date: 当前计算日期（结束日期）
    :return: 间隔年数及天数
    """
    base_time_obj = datetime.datetime.strptime(base_date, format)
    cur_time_obj = datetime.datetime.strptime(cur_date, format)
    gap_obj = relativedelta(dt1=cur_time_obj, dt2=base_time_obj)
    gap_year_days = (cur_time_obj - base_time_obj).days
    gap_hours = gap_obj.hours + gap_obj.days * 24
    result_dict = {
        'hours': gap_hours,
        'minutes': gap_obj.minutes + gap_hours * 60,
        'days': gap_year_days,
    }

    return result_dict.get(count_type)


def subtract_time_period(main_start, main_end, sub_start, sub_end):
    # 转换为时间格式
    main_start = datetime.datetime.strptime(main_start, FORMAT_DATETIME)
    main_end = datetime.datetime.strptime(main_end, FORMAT_DATETIME)
    sub_start = datetime.datetime.strptime(sub_start, FORMAT_DATETIME)
    sub_end = datetime.datetime.strptime(sub_end, FORMAT_DATETIME)
    # 如果没有交集，返回原始时间段
    if main_end <= sub_start or main_start >= sub_end:
        return [(str(main_start), str(main_end))]

    time_periods = []

    # 如果主时间段开始时间早于子时间段开始时间
    if main_start < sub_start:
        time_periods.append((str(main_start), str(sub_start)))

    # 如果主时间段结束时间晚于子时间段结束时间
    if main_end > sub_end:
        time_periods.append((str(sub_end), str(main_end)))

    return time_periods


def generate_week(date_str=None):
    if not date_str:
        date_str = time.strftime(FORMAT_DATE, time.localtime())
    a = time.strptime(date_str, FORMAT_DATE)  # date_str为给定的日期例如（2022-09-22）
    y = a.tm_year
    m = a.tm_mon
    d = a.tm_mday
    week_num = datetime.datetime(int(y), int(m), int(d)).isocalendar()[1]  # 一年中的第几周
    return week_num


def generate_year(date_str):
    if date_str:
        if int(generate_week(date_str)) > 50 and int(date_str[5:7]) < 2:
            return str(int(date_str[0:4]) - 1)
        else:
            return date_str[0:4]
    else:
        return None


def generate_md5(data_list):
    data_str = ''
    for i in data_list:
        data_str += str(i).strip()
    hash_obj = hashlib.md5()
    hash_obj.update(data_str.encode())
    return hash_obj.hexdigest()


def generate_uuid():
    return str(uuid.uuid1())


def async_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tms_execute = ThreadPoolExecutor(2)
        tms_execute.submit(func, *args, **kwargs)

    return wrapper


def calculate_full_day_between_two_dates(start_time, end_time):
    start_date = datetime.datetime.strptime(str(start_time)[0:10], FORMAT_DATE)
    end_date = datetime.datetime.strptime(str(end_time)[0:10], FORMAT_DATE)
    num = (end_date - start_date).days
    return num - 1


def create_connection(config):
    conn = pymysql.connect(**config)
    curr = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn, curr


global_logger = InitLog().create_log()


def activate_redis_client():
    while True:
        try:
            redis_client = redis.StrictRedis(**redis_config)
            redis_client.ping()
            global_logger.info('Redis is available, start application ... ')
            return redis_client
        except redis.exceptions.ConnectionError:
            global_logger.error('Redis is Not Available, retry ... ')
            time.sleep(2)


op11_redis_client = activate_redis_client()


def conditional_filter(filter_list, field, value):
    if isinstance(value, str):
        filter_list.append(field.contains(value))
    elif isinstance(value, list):
        filter_list.append(field.in_(value))
    elif isinstance(value, int):
        filter_list.append(field == value)


def update_tool(update_dict, params, update_key, mtc):
    for key in update_key:
        if key not in params.keys():
            continue
        update_dict[key] = params.get(key, getattr(mtc, key))


def calculate_time_to_finish(user_time, percent):
    return round((user_time / percent) * (1 - percent))


def get_first_and_last_day(year, month):
    week_day, month_count_day = calendar.monthrange(year, month)
    first_day = datetime.date(year, month, day=1)
    last_day = datetime.date(year, month, day=month_count_day)
    return first_day.strftime(f"{FORMAT_DATE}"), last_day.strftime(f"{FORMAT_DATE}")
