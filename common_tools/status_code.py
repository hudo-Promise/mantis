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
    200: 'success',
    300: 'missing credentials, please login',
    10001: 'user already exists',
    10002: 'user name is empty',
    10003: 'user password is invalid',
    10004: 'user project or role is empty',
    10005: 'user does not exist',
    10006: 'password incorrect',
    10007: 'email format is invalid',
    10008: 'The current user does not have permission to modify user roles',
    10009: 'The current user does not have permission to add user',
    10010: 'You do not have permission to complete this action.',
    10011: 'Error Batch add',
    10012: 'This application cannot be recalled',
    10013: 'The current leave is not editable',
    10014: 'The currently selected date already has an application',
    10015: "The currently selected date doesn't have workday",
    10016: "There some error in our server",
    10017: "This period would be available after updating VGC holidays.",
    10018: 'The currently selected date does not comply with overtime rules',
    10019: 'Project and role do not match',
    10020: 'user already invited',
    10021: 'The registration link has expired',
    10022: 'User information mismatch',
    10023: 'Verification code error or expired',
    10024: 'Verification code has been send,please check in email',
    10025: 'No viewing permission',
    10026: 'Input format is not right',
}
