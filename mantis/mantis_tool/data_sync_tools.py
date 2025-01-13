from mantis.mantis_tool.async_task_tools import async_task_new
from mantis.models.case import TestCase, CaseResult, MantisForKpmMap
from mantis.models.functions import MantisCaseField
from common_tools.tools import global_logger
from common_tools.free_log_handle import async_send_free_log
from common_tools.excel_tool import CreateExcelTools
from datetime import datetime
import requests
from requests_toolbelt import MultipartEncoder
from io import BytesIO
import traceback

from config.basic_setting import SERVICE_MODE, KPM_HCP3_PERF_API


def get_config_for_hcp3():
    hcp3_config = MantisForKpmMap.query.filter().all()
    hcp3_config_dict = {item.sub_category: item.to_dict() for item in hcp3_config}
    test_platform_config = MantisCaseField.query.filter(MantisCaseField.case_field == 'test_platform').first()
    if test_platform_config:
        test_platform_dict = test_platform_config.case_field_mapping
    else:
        test_platform_dict = {}
    test_carline_config = MantisCaseField.query.filter(MantisCaseField.case_field == 'test_carline').first()
    if test_carline_config:
        test_carline_dict = test_carline_config.case_field_mapping
    else:
        test_carline_dict = {}
    return hcp3_config_dict, test_platform_dict, test_carline_dict


def get_sync_case_data(test_sw_list=None):
    case_filter_list = [
        TestCase.cluster.in_([1, 4]), TestCase.sub_function == 65, TestCase.level == 2
    ]
    hcp3_case_objs = TestCase.query.filter(*case_filter_list).all()
    hcp3_case_dict = {case_obj.id: case_obj.to_dict() for case_obj in hcp3_case_objs}
    case_result_filter_list = [
        CaseResult.m_id.in_(list(hcp3_case_dict.keys())), CaseResult.test_result.in_([1, 2, 3])
    ]
    if test_sw_list:
        case_result_filter_list.append(CaseResult.test_sw.in_(test_sw_list))
    hcp3_case_result_objs = CaseResult.query.filter(*case_result_filter_list).all()
    return hcp3_case_dict, hcp3_case_result_objs


def get_sync_headers():
    return ['Function', 'Feature', 'Sub_Category', 'Category', 'Level', 'Original requirement in ms',
            'Time(ms)',
            'Car Model', 'Test time(YY-MM)', 'Car Id', 'SW Version', 'Brand', 'Comment']


def get_upload_hcp3_data_dict(hcp3_case_dict, hcp3_case_result_objs, hcp3_config_dict, test_platform_dict,
                              test_carline_dict, trans_headers):
    """获取hcp3上传数据结果"""
    trans_result = dict()
    for hcp3_case_result_obj in hcp3_case_result_objs:
        case_data = hcp3_case_dict.get(hcp3_case_result_obj.m_id, {})
        if not case_data:
            continue
        sub_category = case_data.get('title')
        category_map = hcp3_config_dict.get(sub_category, {})
        function = category_map.get('function', '')
        feature = category_map.get('feature', '')
        category = category_map.get('category', '')
        level = 'F6'
        expectation = case_data.get('expectation', '')
        expectation_time = expectation.split('ms', 1)
        if len(expectation_time) > 0:
            expectation_time = expectation_time[0].strip()
        else:
            expectation_time = ''
        if hcp3_case_result_obj.test_result == 3:
            time = 'TB'
        else:
            time = hcp3_case_result_obj.extra_1
        car_model = test_platform_dict.get(str(hcp3_case_result_obj.test_platform))
        test_time = datetime.strftime(hcp3_case_result_obj.create_time, "%Y/%m/%d")
        car_id = test_carline_dict.get(str(hcp3_case_result_obj.test_carline))
        sw_version = hcp3_case_result_obj.test_sw.title()
        brand = 'Audi'
        comment = hcp3_case_result_obj.comments
        trans_result.setdefault(sw_version, [trans_headers]).append(
            [function, feature, sub_category, category, level, expectation_time, time, car_model, test_time, car_id,
             sw_version, brand, comment])
    return trans_result


def upload_hcp3_version_data(version, trans_list_data):
    """上传指定version结果"""
    try:
        all_data_dict = {
            version: trans_list_data
        }
        filename = f'./HCP3_{version}.xlsx'
        virtual_workbook = BytesIO()
        CreateExcelTools.save_sample_data(virtual_workbook, all_data_dict)
        virtual_workbook.seek(0)

        m = MultipartEncoder(fields={
            "verify": '0',
            "project": "HCP3",
            "file": (
                filename, virtual_workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")})
        response = requests.post(KPM_HCP3_PERF_API, data=m, headers={'Content-Type': m.content_type}, timeout=20)
        if response.status_code == 200:
            res = response.json()
            if res.get('msg') == '上传文件成功':
                return {'sync_status': 'success', 'sync_version': version, 'sync_num': len(trans_list_data) - 1}, 1
            else:
                return {'sync_status': 'failed', 'sync_version': version, 'sync_num': len(trans_list_data) - 1}, 0
        else:
            return {'sync_status': 'failed', 'sync_version': version, 'sync_num': len(trans_list_data) - 1,
                    'msg': 'kpm net error'}, 0

    except:
        global_logger.error(traceback.format_exc())
        return {'sync_status': 'error', 'sync_version': version, 'sync_num': len(trans_list_data) - 1,
                'error_msg': traceback.format_exc()}, 0


def upload_hcp3_data(trans_result):
    """上传所有结果"""
    sync_log = []
    status = 1
    for version, trans_list_data in trans_result.items():
        upload_log, upload_status = upload_hcp3_version_data(version, trans_list_data)
        sync_log.append(upload_log)
        if upload_status == 0:
            status = 0
    return sync_log, status


@async_task_new('mantis')
def run_sync_mantis_hcp3_data_to_kpm(test_sw_list=None):
    """同步mantis所有符合条件的数据（hcp3）到kpm"""
    log_time = str(datetime.now())
    try:
        # 读取配置
        hcp3_config_dict, test_platform_dict, test_carline_dict = get_config_for_hcp3()
        # 获取传输数据
        hcp3_case_dict, hcp3_case_result_objs = get_sync_case_data(test_sw_list)
        trans_headers = get_sync_headers()
        # 生成传输数据结构
        trans_result = get_upload_hcp3_data_dict(hcp3_case_dict, hcp3_case_result_objs, hcp3_config_dict,
                                                 test_platform_dict,
                                                 test_carline_dict, trans_headers)

        sync_log, status = upload_hcp3_data(trans_result)
        if status == 0:
            log_level = 'WARNING'
        else:
            log_level = 'INFO'
        error_message = ''
    except:
        sync_log = []
        log_level = 'ERROR'
        error_message = traceback.format_exc()
    try:
        log_data = {
            "service": "mantis",
            "env": SERVICE_MODE,
            "log_source": "backend",
            "log_type": "TASK",
            "request_path": 'run_sync_mantis_hcp3_data_to_kpm',
            "request_method": 'run_sync_mantis_hcp3_data_to_kpm',
            "method_name": 'run_sync_mantis_hcp3_data_to_kpm',
            "log_level": log_level,
            "log_time": log_time,
            "error_message": error_message,
            "additional_data": {
                "sync_log": sync_log
            }
        }
        async_send_free_log(log_data)
    except:
        global_logger.error(traceback.format_exc())
