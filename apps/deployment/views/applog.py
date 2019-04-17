# @Time    : 2019/4/1 13:50
# @Author  : xufqing
from rest_framework.views import APIView
from rest_xops.basic import XopsResponse
from rest_xops.code import *
from common.custom import RbacPermission
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.shell_excu import connect_init
from django.http import FileResponse
from rest_framework.renderers import BaseRenderer
import os

class PassthroughRenderer(BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = ''
    format = ''
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class AppLogView(APIView):
    '''
    远程应用日志
    '''
    perms_map = ({'*': 'admin'}, {'*': 'deploy_all'}, {'post': 'applog_list'})
    permission_classes = (RbacPermission,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, format=None):
        if request.data['excu'] == 'list':
            try:
                app_log_path = request.data['app_log_path']
                host = request.data['host']
                connect = connect_init(host)
                commands = "find %s -name '*.log'" % (app_log_path)
                result = connect.run(commands).stdout
                res = []
                for i in result.split():
                    res.append(i)
                res = filter(None, res)
                connect.close()
                http_status = OK
            except Exception as e:
                http_status = BAD
                res = '执行错误:' + str(e)
            return XopsResponse(res, status=http_status)

        elif request.data['excu'] == 'filedown':
            file_path = request.data['file_path']
            host = request.data['host']
            file_name = os.path.basename(file_path)
            dir_name = os.path.dirname(file_path)
            old_file_name = os.path.splitext(file_name)
            if old_file_name[1] == '.log':
                new_file_name = old_file_name[0] + '.tar.gz'
                connect = connect_init(host)
                commands = 'mkdir -p /tmp/remote/ && tar czf /tmp/remote/%s -C %s %s' % (new_file_name, dir_name, file_name)
                connect.run(commands)
                connect.get('/tmp/remote/' + new_file_name ,'/tmp/' + new_file_name)
                response = FileResponse(open('/tmp/' + new_file_name, 'rb'))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="%s"' % old_file_name[0]
                commands = 'rm -f /tmp/remote/%s' % (new_file_name)
                connect.run(commands)
                connect.close()
                os.remove('/tmp/' + new_file_name)
                return response
            else:
                return XopsResponse('请求文件格式不对!',status=BAD)