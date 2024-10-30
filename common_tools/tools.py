import calendar
import datetime
import hashlib
import json
import re
import time
import uuid
from concurrent.futures.thread import ThreadPoolExecutor
from functools import wraps
from dateutil.relativedelta import relativedelta
import pymysql
import redis
from chinese_calendar import is_holiday

from common_tools.logger import InitLog
from config.basic_setting import redis_config, FORMAT_DATE, FORMAT_DATETIME


def create_current_format_time():
    return time.strftime(FORMAT_DATETIME, time.localtime())


def check_is_bigger_time(cur_time, check_time, add_time=None, add_time_type='hours', format=FORMAT_DATETIME):
    """
    判断字符串时间是否大于后者
    :param cur_time: 当前时间
    :param check_time:被判断时间
    :param add_time:加减时间 +7 -9
    :param add_time_type:加减时间类型 hours days
    :param format:时间格式
    :return:
    """
    cur_time = datetime.datetime.strptime(cur_time, format)
    check_time = datetime.datetime.strptime(check_time, format)
    if add_time:
        time_dict = {add_time_type: add_time}
        check_time = check_time + relativedelta(**time_dict)
    if cur_time >= check_time:
        return True
    else:
        return False


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


def has_overlap(start_a, end_a, start_b, end_b):
    """判断两个时间段是否有交集"""
    start_a = datetime.datetime.strptime(start_a, FORMAT_DATETIME)
    end_a = datetime.datetime.strptime(end_a, FORMAT_DATETIME)
    start_b = datetime.datetime.strptime(start_b, FORMAT_DATETIME)
    end_b = datetime.datetime.strptime(end_b, FORMAT_DATETIME)
    return start_a < end_b and end_a > start_b


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


def count_holiday_gaps(start_time, end_time):
    cur_day = start_time.split(' ')[0]
    new_periods = subtract_time_period(start_time, end_time, f'{cur_day} 12:00:00', f'{cur_day} 13:00:00')
    gap_hours = 0
    for period in new_periods:
        gap_hours += get_gap_days(period[0], period[1], count_type='hours')


def create_before_of_day_time(n):
    today = datetime.datetime.now()
    offset = datetime.timedelta(days=-n)
    result = (today + offset).strftime(FORMAT_DATE) + ' 00:00:00'
    return result


def create_offset_format_time(n, target_datetime=None):
    offset = datetime.timedelta(days=n)
    if not target_datetime:
        target_datetime = datetime.datetime.now()
    else:
        target_datetime = datetime.datetime.strptime(target_datetime, FORMAT_DATETIME)
    result = (target_datetime + offset).strftime(FORMAT_DATETIME)
    return result


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


def specific_time_format(value, time_type):
    if time_type == 'date':
        pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    elif time_type == 'datetime':
        pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    else:
        pattern = re.compile(r'--------------')
    result = pattern.match(str(value))
    if result:
        return True
    else:
        return False


def generate_md5(data_list):
    data_str = ''
    for i in data_list:
        data_str += str(i).strip()
    hash_obj = hashlib.md5()
    hash_obj.update(data_str.encode())
    return hash_obj.hexdigest()


def generate_uuid():
    return str(uuid.uuid1())


def calculate_duration_nodes(start_time, end_time):
    start_date = datetime.datetime.strptime(str(start_time)[:10], FORMAT_DATE)
    end_date = datetime.datetime.strptime(str(end_time)[:10], FORMAT_DATE)
    start_stamp = int(datetime.datetime.strptime(str(start_time), FORMAT_DATETIME).timestamp())
    end_stamp = int(datetime.datetime.strptime(str(end_time), FORMAT_DATETIME).timestamp())
    start_work_stamp = int(time.mktime(time.strptime(str(end_time)[:10] + ' 08:30:00', FORMAT_DATETIME)))
    end_work_stamp = int(time.mktime(time.strptime(str(start_time)[:10] + ' 17:30:00', FORMAT_DATETIME)))
    start_lunch_stamp = int(time.mktime(time.strptime(str(end_time)[:10] + ' 12:00:00', FORMAT_DATETIME)))
    end_lunch_stamp = int(time.mktime(time.strptime(str(start_time)[:10] + ' 13:00:00', FORMAT_DATETIME)))
    if start_date == end_date:
        if start_stamp > end_lunch_stamp or end_stamp < start_lunch_stamp:
            work_second = abs(start_stamp - end_stamp)
        else:
            work_second = abs(start_stamp - end_stamp) - 3600
        return work_second
    else:
        if start_stamp < start_lunch_stamp and end_stamp < start_lunch_stamp:
            work_second = abs(start_stamp - end_work_stamp) + abs(start_work_stamp - end_stamp) - 3600
        elif start_stamp > end_lunch_stamp and end_stamp > end_lunch_stamp:
            work_second = abs(start_stamp - end_work_stamp) + abs(start_work_stamp - end_stamp) - 3600
        elif start_stamp > end_lunch_stamp and end_stamp < start_lunch_stamp:
            work_second = abs(start_stamp - end_work_stamp) + abs(start_work_stamp - end_stamp)
        else:
            work_second = abs(start_stamp - end_work_stamp - 1) + abs(start_work_stamp - end_stamp - 1) - 2 * 3600

        if (start_date + datetime.timedelta(days=1)) == end_date:
            return work_second
        else:
            interval_days = abs((start_date - end_date).days) - 1
            days = [start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)]
            for day in days:
                if is_holiday(day):
                    interval_days -= 1
            work_second += 3600 * 8 * interval_days
            return work_second


def async_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tms_execute = ThreadPoolExecutor(2)
        tms_execute.submit(func, *args, **kwargs)

    return wrapper


def verify_format_time_is_holiday(format_time):
    specific_all = ['12-25']
    specific_half = ['2024-02-09', '2024-12-24', '2024-12-31']
    current_date = datetime.datetime.strptime(str(format_time), FORMAT_DATE).date()
    if str(format_time)[5:] in specific_all:
        return True, True
    if str(format_time) in specific_half:
        return True, False
    return is_holiday(current_date), True


def calculate_full_day_between_two_dates(start_time, end_time):
    start_date = datetime.datetime.strptime(str(start_time)[0:10], FORMAT_DATE)
    end_date = datetime.datetime.strptime(str(end_time)[0:10], FORMAT_DATE)
    num = (end_date - start_date).days
    return num - 1


def generate_dates(start_date, end_date):
    start = datetime.datetime.strptime(start_date, FORMAT_DATE)
    end = datetime.datetime.strptime(end_date, FORMAT_DATE)
    day = datetime.timedelta(days=1)
    for i in range((end - start).days + 1):
        yield start + day * i


def generate_date_by_week(year, week, n):
    format_str = f'{year}-W{week}-{n}'
    week_date = datetime.datetime.strptime(format_str, '%Y-W%W-%w').strftime(FORMAT_DATE)
    return week_date


def generate_week_by_date(date_time):
    week = datetime.datetime.strptime(date_time, FORMAT_DATE).strftime("%W")
    return week


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


def clear_schedule_user(receivers, cc, project):
    receivers, cc = list(set(receivers)), list(set(cc))
    schedule_email = json.loads(op11_redis_client.get('tms_schedule_email'))
    for key, value in schedule_email.items():
        if not value.get(str(project)):
            continue
        if value.get(str(project)).get('account') in receivers:
            receivers.remove(value.get(str(project)).get('account'))
        if value.get(str(project)).get('account') in cc:
            cc.remove(value.get(str(project)).get('account'))
    return receivers, cc


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
