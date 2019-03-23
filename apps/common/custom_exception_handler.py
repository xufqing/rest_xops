# @Time    : 2019/2/13 17:31
# @Author  : xufqing
from rest_framework.views import exception_handler

'''
自定义异常response返回结果
'''
def notification_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        notification_response = {}
        notification_response['detail'] = response.data
        response.data = notification_response

    return response