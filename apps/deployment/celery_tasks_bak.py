# @Time    : 2019/3/22 0:27
# @Author  : xufqing
from deployment.models import Project, DeployRecord
from cmdb.models import ConnectionInfo, DeviceInfo
from utils.shell_excu import Shell
from utils.common import includes_format, excludes_format
import utils.globalvar as gl
from celery import Task
from rest_xops.celery import app
from utils.websocket_tail import Tailf
from django.conf import settings

class DeployExcu(Task):
    _path = settings.WORKSPACE
    sequence = 0
    release_version = None
    prev_release_version = None
    result = None
    file = None

    def deploy_init(self, webuser, record_id, id=None):
        self.localhost = Shell('127.0.0.1')
        if id:
            project = Project.objects.filter(id=int(id)).values()
            self.project_id = project[0]['id']
            self.alias = str(project[0]['alias'])
            self.repo_url = str(project[0]['repo_url'])
            self.local_code_path = self._path + str(id) + '_' + str(project[0]['alias']) + '/' + str(
                project[0]['alias'])
            self.local_project_path = self._path + str(id) + '_' + str(project[0]['alias'])
            self.local_log_path = self._path + str(id) + '_' + str(project[0]['alias']) + '/logs'
            self.is_include = project[0]['is_include']
            self.excludes = project[0]['excludes']
            self.task_envs = project[0]['task_envs']
            self.prev_deploy = project[0]['prev_deploy']
            self.post_deploy = project[0]['post_deploy']
            self.prev_release = project[0]['prev_release']
            self.post_release = project[0]['post_release']
            self.target_root = project[0]['target_root']
            self.target_releases = project[0]['target_releases']
            self.version_num = project[0]['version_num']
            self.custom_global_env = {
                'WEB_ROOT': str(self.target_root),
                'CODE_ROOT': str(self.local_code_path),
                'ALIAS': str(self.alias)
            }
            if project[0]['task_envs']:
                task_envs = [i.strip() for i in project[0]['task_envs'].split('\n') if
                             i.strip() and not i.strip().startswith('#')]
                for var in task_envs:
                    var_list = var.split('=', 1)
                    if len(var_list) != 2:
                        continue
                    self.custom_global_env[var_list[0]] = var_list[1]
            self.localhost.init_env(env=self.custom_global_env)
            self.webuser = webuser
            self.record_id = record_id

    def do_prev_deploy(self, log):
        '''
        代码检出前要做的基础工作
        '''
        self.sequence = 1
        with open(log, 'a') as f:
            f.write('[INFO]------正在执行代码检出前的工作------%s\n' % (self.sequence))
        commands = self.prev_deploy
        if commands:
            for command in commands.split('\n'):
                if command.strip().startswith('#') or not command.strip():
                    continue
                with self.localhost.cd(self.local_code_path):
                    self.result = self.localhost.local(command, write=log)

    def do_checkout(self, version, log):
        '''
        检出代码
        '''
        if self.result.exited == 0:
            self.sequence = 2
            with open(log, 'a') as f:
                f.write('[INFO]------正在执行代码检出------%s\n' % (self.sequence))

            # 更新到指定 commit
            with self.localhost.cd(self.local_code_path):
                self.result = self.localhost.local('git fetch --all', write=log)
                command = 'git rev-parse %s' % (version)
                commit_id = self.localhost.local(command, write=log).stdout.strip()
                command = 'git checkout -f %s' % (commit_id)
                if self.result.exited == 0:
                    self.result = self.localhost.local(command, write=log)

    def do_post_deploy(self, log):
        '''
        检出代码后的工作：如编译
        '''
        if self.result.exited == 0:
            self.sequence = 3
            with open(log, 'a') as f:
                f.write('[INFO]------正在执行代码检出后的工作------%s\n' % (self.sequence))
            commands = self.post_deploy
            if commands:
                for command in commands.split('\n'):
                    if command.strip().startswith('#') or not command.strip():
                        continue
                    with self.localhost.cd(self.local_code_path):
                        if self.result.exited == 0:
                            self.result = self.localhost.local(command, write=log)
            # 打包编译后的文件：包含或排除
            self.release_version = self.record_id
            with self.localhost.cd(self.local_code_path):
                if self.is_include:
                    files = includes_format(self.local_code_path, self.excludes)
                    command = 'tar zcf %s/%s %s' % (
                        self.local_project_path.rstrip('/'), self.release_version + '.tar.gz', files)
                else:
                    files = excludes_format(self.local_code_path, self.excludes)
                    command = 'tar zcf ../%s %s' % (self.release_version + '.tar.gz', files)
                if self.result.exited == 0:
                    self.result = self.localhost.local(command, write=log)

    def do_prev_release(self, log, connect):
        '''
        部署代码到目标机器前执行
        '''
        if self.result.exited == 0:
            self.sequence = 4
            with open(log, 'a') as f:
                f.write('[INFO]------正在执行部署前的工作------%s\n' % (self.sequence))
            # 创建远程target_releases目录
            command = '[ -d %s ] || mkdir -p %s' % (self.target_releases, self.target_releases)
            if self.result.exited == 0:
                self.result = connect.run(command, write=log)
            # 上传压缩包
            self.file = '%s/%s' % (self.local_project_path.rstrip('/'), self.release_version + '.tar.gz')
            if self.result.exited == 0:
                connect.put(self.file, remote=self.target_releases, write=log)

            # 判断是否超过可存档的数量
            with connect.cd(self.target_releases):
                command = 'ls -l |grep "^d"|wc -l'
                if self.result.exited == 0:
                    self.result = connect.run(command, write=log)
                releases_num = int(self.result.stdout.strip())
                if releases_num >= self.version_num:
                    last_data = DeployRecord.objects.filter(project_id=self.project_id, name__contains='部署',
                                                            status='Succeed',
                                                            is_rollback=True).order_by('-id')[
                                :self.version_num].values()
                    last_record_id = last_data[self.version_num - 1]['record_id']
                    command = 'rm -rf %s/%s' % (self.target_releases, last_record_id)
                    if self.result.exited == 0:
                        self.result = connect.run(command, write=log)
                        DeployRecord.objects.filter(id=last_data[self.version_num - 1]['id']).update(is_rollback=False)

            # 解压并删除压缩源
            with connect.cd(self.target_releases):
                command = 'mkdir %s && tar zxf %s -C %s && rm -f %s' % \
                          (self.release_version, self.release_version + '.tar.gz', self.release_version,
                           self.release_version + '.tar.gz')
                if self.result.exited == 0:
                    self.result = connect.run(command, write=log)

            # 执行自定义命令
            commands = self.prev_release
            if commands:
                for command in commands.split('\n'):
                    if command.strip().startswith('#') or not command.strip():
                        continue
                    target_release_version = "%s/%s" % (self.target_releases, self.release_version)
                    with connect.cd(target_release_version):
                        if self.result.exited == 0:
                            self.result = connect.run(command, write=log)

    def do_release(self, log, connect):
        '''
        执行部署到目标机器：生成软链等
        '''
        if self.result.exited == 0:
            self.sequence = 5
            with open(log, 'a') as f:
                f.write('[INFO]------正在执行部署工作------%s\n' % (self.sequence))
            # 创建远程target_root目录
            command = '[ -d %s ] || mkdir -p %s' % (self.target_root, self.target_root)
            if self.result.exited == 0:
                self.result = connect.run(command, write=log)
            # 检查上次的版本
            with connect.cd(self.target_releases):
                version_file = '%s/%s' % (self.target_root, self.alias + '_version.txt')
                command = 'touch %s && cat %s' % (version_file, version_file)
                if self.result.exited == 0:
                    self.result = connect.run(command, write=log)
                    self.prev_release_version = self.result.stdout

            # 如果存在旧版本，则删除软链
            if self.prev_release_version:
                command = 'find %s -type l -delete' % (self.target_root)
                if self.result.exited == 0:
                    self.result = connect.run(command, write=log)
            # 创建当前版本软链到webroot
            command = 'ln -sfn %s/%s/* %s && echo %s > %s' % (self.target_releases,
                                                              self.release_version, self.target_root,
                                                              self.release_version, version_file)
            if self.result.exited == 0:
                self.result = connect.run(command, write=log)

    def do_post_release(self, log, connect):
        '''
        部署代码到目标机器后执行
        '''
        if self.result.exited == 0:
            self.sequence = 6
            with open(log, 'a') as f:
                f.write('[INFO]------正在执行部署后的工作------%s\n' % (self.sequence))
            commands = self.post_release
            if commands:
                for command in commands.split('\n'):
                    if command.strip().startswith('#') or not command.strip():
                        continue
                    with connect.cd(self.target_root):
                        pty = False if command.find('nohup') >= 0 else True
                        if self.result.exited == 0:
                            self.result = connect.run(command, pty=pty, write=log)
            connect.close()

    def end(self, server_ids, record_id):
        if self.localhost:
            # 删除打包的源文件
            self.localhost.local('rm -f %s' % (self.file))
            # 关闭连接
            self.localhost.close()
        # 关闭死循环读取本地日志
        gl.set_value('deploy_' + str(self.webuser), True)
        sid = ','.join(server_ids)
        defaults = {
            'record_id': record_id,
            'alias': self.alias,
            'server_ids': sid,
            'target_root': self.target_root,
            'target_releases': self.target_releases,
            'prev_record': self.prev_release_version.strip(),
            'is_rollback': True,
            'status': 'Succeed'
        }
        name = '部署_' + record_id
        if self.result.exited == 0:
            DeployRecord.objects.filter(name=name).update(**defaults)
        else:
            defaults['status'] = 'Failed'
            defaults['is_rollback'] = False
            DeployRecord.objects.filter(name=name).update(**defaults)

    def start(self, log, version, serverid, record_id, webuser):
        try:
            self.do_prev_deploy(log)
            self.do_checkout(version, log)
            self.do_post_deploy(log)
            for sid in serverid:
                try:
                    device_info = DeviceInfo.objects.filter(id=int(sid)).values()
                    host = device_info[0]['hostname']
                    auth_type = device_info[0]['auth_type']
                    connect_info = ConnectionInfo.objects.filter(hostname=host, auth_type=auth_type).values()
                    user = connect_info[0]['username']
                    passwd = connect_info[0]['password']
                    port = connect_info[0]['port']
                    auth_info = '{user}@{host}:{port}'.format(user=user, host=host, port=port)
                    auth_key = {auth_type: passwd}
                    connect = Shell(auth_info, connect_timeout=5, connect_kwargs=auth_key)
                    self.do_prev_release(log, connect)
                    self.do_release(log, connect)
                    self.do_post_release(log, connect)
                except Exception as e:
                    send = Tailf()
                    send.send_message(webuser, str(e))
            self.end(serverid, record_id)
        except Exception as e:
            send = Tailf()
            send.send_message(webuser, str(e))

    def run(self, id, log, version, serverid, record_id, webuser):
        self.deploy_init(webuser,record_id,id)
        self.start(log, version, serverid, record_id, webuser)

DeployTask = app.register_task(DeployExcu())