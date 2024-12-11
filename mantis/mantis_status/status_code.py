# -*- coding: utf-8 -*-
class ResponseStruct(object):
    def __init__(self, code, data=None):
        self.code = code
        self.data = data

    def generate(self):
        result = {"code": self.code, "msg": status_code_massage[self.code], "data": self.data}
        return result


def response(code, data=None):
    rs = ResponseStruct(code, data)
    return rs.generate()


status_code_massage = {
    200: 'Execute succeeded',
    300: 'Retry after login',
    404: 'The current page does not exist',
    500: 'The server is not responding',
    10001: 'The account does not exist',
    10002: 'Incorrect password',
    10003: 'Upload failed',
    10004: 'Cannot be empty',
    10005: 'Cluster selection error',
    10006: 'Kanban status selection error',
    10007: 'The key is incorrect',
    10008: 'Submission failed',
    10009: 'board does not exist',
    10010: 'no milestones configured',
    10011: 'Sheet1 not exists, please check your excel',
    10012: 'unknown error',
    10013: 'Delete failed',
    10014: 'Invalid number of columns or invalid cell values',
    10015: 'The data is being calculated',
    10016: 'Invalid result',
}
"""
    200: '执行成功',
    300: '登陆后重试',
    404: '当前页面不存在',
    500: '服务器暂无响应',
    10001: '该账号不存在',
    10002: '密码不正确',
    10003: '上传失败',
    10004: '不能为空',
    10005: '集群选择错误',
    10006: '看板状态选择错误',
    10007: '密钥不正确',
    10008: '提交失败',
    10009: '看板不存在'
    10010: '没有配置里程碑'
    10011: 'sheet页不存在'
"""
