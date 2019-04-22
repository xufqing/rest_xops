# @Time    : 2019/3/4 15:41
# @Author  : xufqing
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_xops.code import *
from rest_xops.basic import XopsResponse
from ..models import Project, DeployRecord
from cmdb.models import DeviceInfo, ConnectionInfo
from utils.shell_excu import Shell, connect_init
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import os, logging, time
from common.custom import CommonPagination, RbacPermission
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers.project_serializer import DeployRecordSerializer
from utils.websocket_tail import Tailf
from ..tasks import deploy
from common.custom import RedisObj
from django.conf import settings
from django.http import FileResponse
from ..tasks import local_tailf

error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class DeployRecordViewSet(ReadOnlyModelViewSet):
    '''
    部署记录：查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'deploy_all'}, {'get': 'deploy_excu'})
    queryset = DeployRecord.objects.all()
    serializer_class = DeployRecordSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('project_id', 'status',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)


class VersionView(APIView):
    perms_map = ({'*': 'admin'}, {'*': 'deploy_all'}, {'get': 'deploy_excu'})
    permission_classes = (RbacPermission,)
    authentication_classes = (JSONWebTokenAuthentication,)
    _path = settings.WORKSPACE

    def get_tag(self, path):
        localhost = Shell('127.0.0.1')
        with localhost.cd(path):
            localhost.local('git fetch --all')
            result = localhost.local('git tag -l')
        return result

    def get_branch(self, path):
        localhost = Shell('127.0.0.1')
        with localhost.cd(path):
            localhost.local('git fetch --all')
            result = localhost.local('git branch -r')
        return result

    def get(self, request, format=None):
        result = None
        id = request.query_params['id']
        repo = Project.objects.filter(id=int(id)).values('alias', 'repo_url', 'repo_mode')
        path = self._path.rstrip('/') + '/' + str(id) + '_' + str(repo[0]['alias']) + '/' + repo[0]['alias']
        if repo[0]['repo_mode'] == 'tag':
            result = self.get_tag(path)
            result = result.stdout.split('\n')
        elif repo[0]['repo_mode'] == 'branch':
            result = self.get_branch(path)
            branches = result.stdout.split('\n')
            result = [branch.strip().lstrip('origin/') for branch in branches if
                      not branch.strip().startswith('origin/HEAD')]
        return XopsResponse(filter(None, result))


class DeployView(APIView):
    '''
    执行部署的逻辑
    '''
    perms_map = ({'*': 'admin'}, {'*': 'deploy_all'}, {'post': 'deploy_excu'})
    permission_classes = (RbacPermission,)
    authentication_classes = (JSONWebTokenAuthentication,)
    _path = settings.WORKSPACE

    def repo_init(self, id):
        if id:
            repo = Project.objects.filter(id=int(id)).values('alias', 'repo_url')
            path = self._path.rstrip('/') + '/' + str(id) + '_' + str(repo[0]['alias'])
            if not os.path.exists(path): os.makedirs(path)
            if not os.path.exists(path + '/logs'): os.makedirs(path + '/logs')
            localhost = Shell('127.0.0.1')
            command = 'cd %s && git rev-parse --is-inside-work-tree' % (repo[0]['alias'])
            with localhost.cd(path):
                result = localhost.local(command)
            if result.exited != 0:
                command = 'rm -rf %s' % (path + '/' + str(repo[0]['alias']))
                localhost.local(command)
                with localhost.cd(path):
                    command = 'git clone %s %s' % (repo[0]['repo_url'], repo[0]['alias'])
                    result = localhost.local(command)
                    massage = '正在克隆%s到%s ...' % (repo[0]['repo_url'], path)
                    info_logger.info(massage)
            localhost.close()
            return result

    def do_rollback(self, id, log, record_id):
        '''
        回滚
        '''
        sequence = 1
        with open(log, 'a') as f:
            f.write('[INFO]------正在执行回滚 [%s]------\n' % (sequence))
        record = DeployRecord.objects.filter(id=int(id)).values()
        is_link = Project.objects.get(id=record[0]['project_id']).is_link
        server_ids = record[0]['server_ids'].split(',')
        name = '回滚_' + str(id) + '_' + record_id
        for sid in server_ids:
            try:
                connect = connect_init(sid)
                version_file = '%s/%s' % (record[0]['target_root'], record[0]['alias'] + '_version.txt')
                # 判断回滚版本是否存在
                command = '[ -d %s/%s ] || echo "false"' % (record[0]['target_releases'], record[0]['prev_record'])
                self.result = connect.run(command, write=log)
                if not self.result.stdout.strip() == 'false':
                    if is_link:
                        # 删除目标软链
                        command = 'find %s -type l -delete' % (record[0]['target_root'])
                        self.result = connect.run(command, write=log)
                        # 创建需回滚版本软链到webroot
                        command = 'ln -sfn %s/%s/* %s' % (
                            record[0]['target_releases'], record[0]['prev_record'], record[0]['target_root'])
                        if self.result.exited == 0: self.result = connect.run(command, write=log)
                    else:
                        command = 'rm -rf %s/*' % (record[0]['target_root'])
                        self.result = connect.run(command, write=log)
                        command = 'cp -r %s/%s/* %s' % (
                            record[0]['target_releases'], record[0]['prev_record'], record[0]['target_root'])
                        if self.result.exited == 0: self.result = connect.run(command, write=log)
                    command = 'echo %s > %s' % (record[0]['prev_record'], version_file)
                    if self.result.exited == 0: self.result = connect.run(command, write=log)
                    with open(log, 'a') as f:
                        f.write('[INFO]------版本已回滚到 [%s]------\n' % (record[0]['prev_record']))
                connect.close()
            except Exception as e:
                error_logger.error(e)

        # 处理完记录入库
        defaults = {
            'name': name,
            'record_id': record[0]['prev_record'],
            'alias': record[0]['alias'],
            'project_id': record[0]['project_id'],
            'server_ids': record[0]['server_ids'],
            'target_root': record[0]['target_root'],
            'target_releases': record[0]['target_releases'],
            'prev_record': record[0]['record_id'],
            'is_rollback': True,
            'status': 'Succeed'
        }
        if self.result.exited != 0 or self.result.stdout.strip() == 'false':
            defaults['status'] = 'Failed'
            defaults['is_rollback'] = False
            DeployRecord.objects.create(**defaults)
            Project.objects.filter(id=record[0]['project_id']).update(last_task_status='Failed')
            with open(log, 'a') as f:
                f.write('[ERROR]------回滚失败------\n')
                f.write('[ERROR]回滚的版本文件可能已删除!\n')
        else:
            DeployRecord.objects.create(**defaults)
            Project.objects.filter(id=record[0]['project_id']).update(last_task_status='Succeed')
            sequence = 6
            with open(log, 'a') as f:
                f.write('[INFO]------回滚完成,请重启应用[%s]------\n' % (sequence))

    def post(self, request, format=None):
        if request.data['excu'] == 'init':
            # 项目初始化
            id = request.data['id']
            result = self.repo_init(id)
            if result.exited == 0:
                Project.objects.filter(id=id).update(status='Succeed')
                info_logger.info('初始化项目:' + str(id) + ',执行成功!')
                http_status = OK
                msg = '初始化成功!'
            else:
                error_logger.error('初始化项目:%s 执行失败! 错误信息:%s' % (str(id), result.stderr))
                http_status = BAD
                msg = '初始化项目:%s 执行失败! 错误信息:%s' % (str(id), result.stderr)

            return XopsResponse(msg, status=http_status)

        elif request.data['excu'] == 'deploy':
            # 部署操作
            id = request.data['id']
            webuser = request.user.username
            alias = request.data['alias']
            self.start_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            record_id = str(alias) + '_' + str(self.start_time)
            name = '部署_' + record_id
            DeployRecord.objects.create(name=name, alias=alias, status='Failed', project_id=int(id))
            Project.objects.filter(id=id).update(last_task_status='Failed')
            local_log_path = self._path.rstrip('/') + '/' + str(id) + '_' + str(request.data['alias']) + '/logs'
            log = local_log_path + '/' + record_id + '.log'
            version = request.data['version'].strip()
            serverid = request.data['server_ids']
            # 调用celery异步任务
            deploy.delay(id, log, version, serverid, record_id, webuser, self.start_time)
            #deploy.run(id, log, version, serverid, record_id, webuser, self.start_time)
            return XopsResponse(record_id)

        elif request.data['excu'] == 'rollback':
            # 回滚
            id = request.data['id']
            project_id = request.data['project_id']
            alias = request.data['alias']
            self.start_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            record_id = str(alias) + '_' + str(self.start_time)
            log = self._path.rstrip('/') + '/' + str(project_id) + '_' + str(alias) + '/logs/' + record_id + '.log'
            self.do_rollback(id, log, record_id)
            return XopsResponse(record_id)

        elif request.data['excu'] == 'deploymsg':
            # 部署控制台消息读取
            try:
                id = request.data['id']
                alias = request.data['alias']
                record = request.data['record']
                scenario = int(request.data['scenario'])
                logfile = self._path.rstrip('/') + '/' + str(id) + '_' + str(alias) + '/logs/' + record + '.log'
                webuser = request.user.username
                if scenario == 0:
                    local_tailf.delay(logfile, webuser, id)
                http_status = OK
                request_status = '执行成功!'
            except Exception as e:
                http_status = BAD
                request_status = str(e)
            return XopsResponse(request_status, status=http_status)

        elif request.data['excu'] == 'readlog' and request.data['scenario'] == 1:
            # 读取部署日志
            try:
                id = request.data['id']
                alias = request.data['alias']
                record = request.data['record']
                logfile = self._path.rstrip('/') + '/' + str(id) + '_' + str(alias) + '/logs/' + record + '.log'
                response = FileResponse(open(logfile, 'rb'))
                response['Content-Type'] = 'text/plain'
                return response
            except Exception:
                http_status = BAD
                request_status = '执行错误:文件不存在!'
            return XopsResponse(request_status, status=http_status)

        elif request.data['excu'] == 'app_start':
            # 项目启动
            try:
                app_start = request.data['app_start']
                host = request.data['host']
                webuser = request.user.username
                connect = connect_init(host)
                app_start = app_start.strip()
                connect.run(app_start, webuser=webuser)
                connect.close()
                http_status = OK
                request_status = '执行成功!'
            except Exception as e:
                http_status = BAD
                request_status = '执行错误:' + str(e)
            return XopsResponse(request_status, status=http_status)

        elif request.data['excu'] == 'app_stop':
            # 项目停止
            try:
                app_stop = request.data['app_stop']
                host = request.data['host']
                webuser = request.user.username
                connect = connect_init(host)
                app_stop = app_stop.strip()
                connect.run(app_stop, webuser=webuser)
                connect.close()
                http_status = OK
                request_status = '执行成功!'
            except Exception as e:
                http_status = BAD
                request_status = '执行错误:' + str(e)
            return XopsResponse(request_status, status=http_status)

        elif request.data['excu'] == 'tail_start':
            # 日志监控
            try:
                filter_text = str(request.data['filter'])
                app_log_file = request.data['app_log_file']
                host = request.data['host']
                webuser = request.user.username
                device_info = DeviceInfo.objects.filter(id=int(host)).values()
                host = device_info[0]['hostname']
                auth_type = device_info[0]['auth_type']
                connect_info = ConnectionInfo.objects.filter(hostname=host, auth_type=auth_type).values()
                user = connect_info[0]['username']
                passwd = connect_info[0]['password']
                port = connect_info[0]['port']
                tail = Tailf()
                tail.remote_tail(host, port, user, passwd, app_log_file, webuser, filter_text=filter_text)
                http_status = OK
                request_status = '执行成功!'
            except Exception as e:
                http_status = BAD
                request_status = str(e)
            return XopsResponse(request_status, status=http_status)

        elif request.data['excu'] == 'tail_stop':
            # 日志监控停止
            try:
                webuser = request.user.username
                redis = RedisObj()
                redis.set('remote_tail_' + str(webuser), '1')
                http_status = OK
                request_status = '执行成功!'
            except Exception as e:
                http_status = BAD
                request_status = str(e)
            return XopsResponse(request_status, status=http_status)
