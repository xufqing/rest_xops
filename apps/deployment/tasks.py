# @Time    : 2019/4/13 8:22
# @Author  : xufqing

from deployment.models import Project, DeployRecord
from utils.shell_excu import Shell, connect_init
from utils.common import includes_format, excludes_format
from utils.websocket_tail import Tailf
from django.conf import settings
import os, time, logging
from celery import Task
from rest_xops.celery import app
from common.custom import RedisObj

error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


@app.task
def local_tailf(logfile, webuser, id):
    info_logger.info('[部署日志监控开始] 文件地址：%s 用户：%s 项目ID：%s' % (logfile, webuser, id))
    redis = RedisObj()
    f = open(logfile, 'rt')
    f.seek(0, 0)
    while True:
        line = f.readline()
        if not line:
            is_stop = redis.get('deploy_' + str(webuser) + '_' + str(id))
            if is_stop == '1':
                Tailf.send_message(webuser, '[INFO]文件监视结束..')
                f.close()
                info_logger.info('[部署日志监控结束] 文件地址：%s 用户：%s 项目ID：%s' % (logfile, webuser, id))
                break
            else:
                time.sleep(0.2)
                continue
        Tailf.send_message(webuser, line)


class DeployExcu(Task):
    name = __name__
    _path = settings.WORKSPACE
    sequence = 0
    release_version = None
    prev_release_version = None
    result = None
    file = None
    start_time = None

    def init(self, webuser, record_id, id=None):
        self.localhost = Shell('127.0.0.1')
        if id:
            project = Project.objects.filter(id=int(id)).values()
            self.project_id = project[0]['id']
            self.alias = str(project[0]['alias'])
            self.environment = str(project[0]['environment'])
            self.repo_url = str(project[0]['repo_url'])
            self.local_code_path = self._path + str(id) + '_' + str(project[0]['alias']) + '/' + str(
                project[0]['alias'])
            self.local_project_path = self._path + str(id) + '_' + str(project[0]['alias'])
            self.local_log_path = self._path + str(id) + '_' + str(project[0]['alias']) + '/logs'
            self.is_include = project[0]['is_include']
            self.excludes = project[0]['excludes']
            self.is_link = project[0]['is_link']
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
                'ALIAS': str(self.alias),
                'START_TIME': str(self.start_time)
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
            f.write('[INFO]------正在执行代码检出前的工作[%s]------\n' % (self.sequence))
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
        self.sequence = 2
        with open(log, 'a') as f:
            f.write('[INFO]------正在执行代码检出[%s]------\n' % (self.sequence))

        # 更新到指定 commit
        with self.localhost.cd(self.local_code_path):
            self.result = self.localhost.local('git checkout master && git pull', write=log)
            command = 'git rev-parse %s' % (version)
            commit_id = self.localhost.local(command, write=log).stdout.strip()
            command = 'git checkout -f %s' % (commit_id)
            if self.result.exited == 0:
                self.result = self.localhost.local(command, write=log)
            command = 'git show --stat'
            if self.result.exited == 0:
                self.result = self.localhost.local(command, write=log)

    def do_post_deploy(self, log):
        '''
        检出代码后的工作：如编译
        '''
        if self.result.exited == 0:
            self.sequence = 3
            with open(log, 'a') as f:
                f.write('[INFO]------正在执行代码检出后的工作[%s]------\n' % (self.sequence))
            commands = self.post_deploy
            if commands:
                for command in commands.split('\n'):
                    if command.strip().startswith('#') or not command.strip():
                        continue
                    with self.localhost.cd(self.local_code_path):
                        if self.result.exited == 0:
                            self.result = self.localhost.local(command, write=log)
            # 打包编译后的文件：包含或排除
            if self.result.exited == 0:
                self.release_version = self.record_id
                with self.localhost.cd(self.local_code_path):
                    if self.is_include:
                        files = includes_format(self.local_code_path, self.excludes)
                        for file in files:
                            dirname = file[0]
                            filename = '.' if file[1] == '*' else file[1]
                            tar_name = self.local_project_path.rstrip('/') + '/' + self.release_version + '.tar'
                            tar_params = 'tar rf' if os.path.exists(tar_name) else 'tar cf'
                            if dirname:
                                command = '%s %s -C %s %s' % (tar_params, tar_name, dirname, filename)
                                if self.result.exited == 0:
                                    self.result = self.localhost.local(command, write=log)
                            else:
                                command = '%s %s %s' % (tar_params, tar_name, filename)
                                if self.result.exited == 0:
                                    self.result = self.localhost.local(command, write=log)
                    else:
                        files = excludes_format(self.local_code_path, self.excludes)
                        command = 'tar cf ../%s %s' % (self.release_version + '.tar', files)
                        if self.result.exited == 0:
                            self.result = self.localhost.local(command, write=log)

    def do_prev_release(self, log, connect):
        '''
        部署代码到目标机器前执行
        '''
        if self.result.exited == 0:
            self.sequence = 4
            with open(log, 'a') as f:
                f.write('[INFO]------正在执行部署前的工作[%s]------\n' % (self.sequence))

            target_release_version = "%s/%s" % (self.target_releases, self.release_version)

            # 创建远程target_releases目录
            command = '[ -d %s ] || mkdir -p %s' % (target_release_version, target_release_version)
            if self.result.exited == 0:
                self.result = connect.run(command, write=log)

            # 上传压缩包
            self.file = '%s/%s' % (self.local_project_path.rstrip('/'), self.release_version + '.tar')
            if self.result.exited == 0:
                with open(log, 'a') as f:
                    f.write('[INFO]------正在上传压缩包至远程服务器------\n')
                self.result = connect.put(self.file, remote=target_release_version, write=log)

            # 删除打包的源文件
            self.localhost.local('rm -f %s' % (self.file))

            # 判断是否超过可存档的数量
            with connect.cd(self.target_releases):
                command = 'ls -l |grep "^d"|wc -l'
                if self.result.remote:
                    self.result = connect.run(command, write=log)
                releases_num = int(self.result.stdout.strip())
                if releases_num >= self.version_num:
                    command = "ls -t |sort -t '_' -k 2 |head -1"
                    if self.result.exited == 0:
                        self.result = connect.run(command, write=log)
                    last_record_id = self.result.stdout.strip()
                    command = 'rm -rf %s/%s' % (self.target_releases, last_record_id)
                    if self.result.exited == 0:
                        self.result = connect.run(command, write=log)
                        DeployRecord.objects.filter(record_id=last_record_id).update(is_rollback=False)

            # 解压并删除压缩源
            with connect.cd(target_release_version):
                command = 'tar xf %s && rm -f %s' % \
                          (self.release_version + '.tar', self.release_version + '.tar')
                if self.result.exited == 0:
                    self.result = connect.run(command, write=log)

            # 执行自定义命令
            commands = self.prev_release
            if commands:
                for command in commands.split('\n'):
                    if command.strip().startswith('#') or not command.strip():
                        continue
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
                f.write('[INFO]------正在执行部署工作[%s]------\n' % (self.sequence))
            # 创建远程target_root目录
            command = '[ -d %s ] || mkdir -p %s' % (self.target_root, self.target_root)
            if self.result.exited == 0:
                self.result = connect.run(command, write=log)
            # 检查上次的版本
            with connect.cd(self.target_root):
                version_file = '%s/%s' % (self.target_root, self.alias + '_version.txt')
                command = 'touch %s && cat %s' % (version_file, version_file)
                if self.result.exited == 0:
                    self.result = connect.run(command, write=log)
                    self.prev_release_version = self.result.stdout

            # 如果存在旧版本，则删除软链或删除文件
            if self.prev_release_version:
                if self.is_link:
                    command = 'find %s -type l -delete' % (self.target_root)
                    if self.result.exited == 0:
                        self.result = connect.run(command, write=log)
                    # 创建当前版本软链到webroot
                    command = 'ln -sfn %s/%s/* %s && echo %s > %s' % (self.target_releases,
                                                                      self.release_version, self.target_root,
                                                                      self.release_version, version_file)
                    if self.result.exited == 0:
                        self.result = connect.run(command, write=log)
                else:
                    command = 'rm -rf %s/*' % (self.target_root)
                    if self.result.exited == 0:
                        self.result = connect.run(command, write=log)
                    # 复制文件到webroot
                    command = 'cp -r %s/%s/* %s && echo %s > %s' % (self.target_releases,
                                                                      self.release_version, self.target_root,
                                                                      self.release_version, version_file)
                    if self.result.exited == 0:
                        self.result = connect.run(command, write=log)
            else:
                if self.is_link:
                    command = 'ln -sfn %s/%s/* %s && echo %s > %s' % (self.target_releases,
                                                                      self.release_version, self.target_root,
                                                                      self.release_version, version_file)
                    if self.result.exited == 0:
                        self.result = connect.run(command, write=log)
                else:
                    command = 'cp -r %s/%s/* %s && echo %s > %s' % (self.target_releases,
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
                f.write('[INFO]------正在执行部署后的工作[%s]------\n' % (self.sequence))
            target_release_version = "%s/%s" % (self.target_releases, self.release_version)

            # 执行自定义命令
            commands = self.post_release
            if commands:
                for command in commands.split('\n'):
                    if command.strip().startswith('#') or not command.strip():
                        continue
                    with connect.cd(target_release_version):
                        if self.result.exited == 0:
                            self.result = connect.run(command, write=log)
            connect.close()

    def end(self, server_ids, record_id):
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
            Project.objects.filter(id=self.project_id).update(last_task_status='Succeed')
        else:
            defaults['status'] = 'Failed'
            defaults['is_rollback'] = False
            DeployRecord.objects.filter(name=name).update(**defaults)
            Project.objects.filter(id=self.project_id).update(last_task_status='Failed')

    def run(self, id, log, version, serverid, record_id, webuser, start_time):
        info_logger.info(
            '[部署任务开始] 开始时间：%s 记录ID：%s 部署版本：%s 用户：%s 项目ID：%s' % (start_time, record_id, version, webuser, id))
        redis = RedisObj()
        redis.set('deploy_' + str(webuser) + '_' + str(id), '0')
        self.init(webuser, record_id, id)
        self.start_time = start_time
        with open(log, 'a') as f:
            f.write('[INFO]版本: %s 执行用户: %s 开始时间: %s\n[INFO]本次部署日志路径: %s\n' % (version, webuser, start_time, log))
        try:
            self.do_prev_deploy(log)
            self.do_checkout(version, log)
            self.do_post_deploy(log)
            for sid in serverid:
                try:
                    connect = connect_init(sid)
                    connect.init_env(env=self.custom_global_env)
                    self.do_prev_release(log, connect)
                    self.do_release(log, connect)
                    self.do_post_release(log, connect)
                except Exception as e:
                    time.sleep(5)
                    Tailf.send_message(webuser, '[ERROR] 服务器为空或ID %s 可能已被删除!' % sid)
                    Tailf.send_message(webuser, '[ERROR] 错误信息:' % e)
                    error_logger.error('[部署任务错误] 开始时间：%s 记录ID：%s 部署版本：%s 用户：%s 项目ID：%s 信息：%s' % (
                    start_time, record_id, version, webuser, id, e))
            self.end(serverid, record_id)
            info_logger.info('[部署任务已结束] 记录ID：%s 部署版本：%s 用户：%s 项目ID：%s' % (record_id, version, webuser, id))
        except Exception as e:
            Tailf.send_message(webuser, '[ERROR] 错误信息: %s' % e)
            error_logger.error('[部署任务错误] 开始时间：%s 记录ID：%s 部署版本：%s 用户：%s 项目ID：%s 信息：%s' % (
            start_time, record_id, version, webuser, id, e))
        finally:
            if self.localhost:
                self.localhost.close()
            # 关闭local_tailf死循环
            redis.set('deploy_' + str(webuser) + '_' + str(id), '1')


deploy = app.register_task(DeployExcu())
