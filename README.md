demo地址: http://demo.xufqing.cn

管理员账号:admin 密码admin@1234

***rest_xops前端教程***

安装npm运行环境(略)

修改你的配置文件

xops_qd_source/config

dev.env.js #开发环境

prod.env.js #生成环境


开发环境：

```
cd rest_xops/xops_qd_source
npm run dev
#接下来启动后端即可进行调试
```


生产环境：
```
cd rest_xops/xops_qd_source
npm run build
```
生产环境将xops_qd_source/dist目录下生成的文件访问你的服务器nginx目录



**rest_xops 后端教程**

安装mysql（略）

安装redis（略）

创建python虚拟环境

- 安装  
yum install git gcc make patch gdbm-devel openssl-devel sqlite-devel readline-devel zlib-devel bzip2-devel libffi-devel -y  

- 多版本管理工具
1. 安装Pyenv 

```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash  

echo 'export PATH="/$HOME/.pyenv/bin:$PATH"'>> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile 
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile 
pyenv install 3.6.8 -v
pyenv virtualenv 3.6.8 rest_xops
cd 你的项目路径
pyenv local rest_xops
```
```
pip install -r requirements.txt
```

登陆MYSQL，创建数据库

```
CREATE DATABASE rest_xops DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```

执行创建表信息

python manage.py makemigrations rbac

python manage.py makemigrations cmdb

python manage.py makemigrations deployment

python manage.py migrate

如果遇到mysql模块的问题

ImportError: libmysqlclient.so.18: cannot open shared object file: No such file or directory

则：

ln -s /usr/local/mysql/lib/libmysqlclient.so.18 /usr/lib64/libmysqlclient.so.18

MYSQL导入初始化数据

mysql> use rest_xops;

source /home/xufeng/rest_xops/InitScripts/rest_xops.sql;


修改管理员密码（必须操作）

python manage.py changepassword admin

安装扫描工具

yum -y install nmap

安装进程管理

yum -y install supervisor


开机启动

systemctl enable supervisord


启动
systemctl start supervisord



开发环境

python manage.py runserver 0.0.0.0:8000

**设置supervisord**
- celery_worker

```
vim /etc/supervisord.d/celery_worker.ini

[program:celery-worker]
command=/home/xufeng/.pyenv/versions/rest_xops/bin/celery worker -A rest_xops -l INFO
directory=/home/xufeng/rest_xops
environment=PATH="/home/xufeng/.pyenv/versions/rest_xops/bin/"
stdout_logfile=/home/xufeng/rest_xops/logs/worker_celery.log
stderr_logfile=/home/xufeng/rest_xops/logs/worker_celery.log
autostart=true
autorestart=true
priority=901

[program:celery-flower]
command=/home/xufeng/.pyenv/versions/rest_xops/bin/celery flower --broker=redis://localhost:6379/1
directory=/home/xufeng/rest_xops
environment=PATH="/home/xufeng/.pyenv/versions/rest_xops/"
stdout_logfile=/home/xufeng/rest_xops/logs/flower_celery.log
stderr_logfile=/home/xufeng/rest_xops/logs/flower_celery.log
autostart=true
autorestart=true
priority=900
```

**生产环境则需以下操作：**
安装nginx（略）

以下所有/home/xufeng/rest_xops 都改为你的项目地址

/home/xufeng/.pyenv/versions/rest_xops 是你的python虚拟环境的版本



**1、安装uwsgi**

```
 cd /home/xufeng/rest_xops
 
 pip install uwsgi

```
**2、设置Uwsgi配置文件**

```
vim /etc/xops_uwsgi.ini

[uwsgi]
chdir = /home/xufeng/rest_xops
module = rest_xops.wsgi
# process-related settings
master = true
processes = 10
socket =127.0.0.1:8000
#http = 0.0.0.0:8000
vacuum = true

```
**设置supervisord**
- xops_uwsgi
```
vim /etc/supervisord.d/xops_uwsgi.ini

[program:xops]
command=/home/xufeng/.pyenv/versions/rest_xops/bin/uwsgi /etc/xops_uwsgi.ini
stdout_logfile=/home/xufeng/rest_xops/logs/xops_uwsgi.log
stderr_logfile=/home/xufeng/rest_xops/logs/xops_uwsgi.log
stdout_logfile_maxbytes = 20MB
autostart=true
autorestart=true
priority=905
```
- xops_asgi
```
vim /etc/supervisord.d/xops_asgi.ini 

[fcgi-program:asgi]
socket=tcp://127.0.0.1:8001
directory=/home/xufeng/rest_xops
command=/home/xufeng/.pyenv/versions/rest_xops/bin/daphne -u /run/daphne/daphne%(process_num)d.sock --fd 0 --access-log - --proxy-headers rest_xops.asgi:application
numprocs=4
process_name=asgi%(process_num)d
autostart=true
autorestart=true
stdout_logfile=/home/xufeng/rest_xops/logs/xops_asgi.log
stderr_logfile=/home/xufeng/rest_xops/logs/xops_asgi.log
stdout_logfile_maxbytes = 20MB
```

重启

supervisorctl reload

systemctl restart supervisord

supervisorctl start all

查看运行状态

supervisorctl status

以下输出为成功

```
[root@xuxu xufeng]# supervisorctl status
asgi:asgi0                       RUNNING   pid 15331, uptime 1:42:43
asgi:asgi1                       RUNNING   pid 15329, uptime 1:42:44
asgi:asgi2                       RUNNING   pid 15343, uptime 1:42:42
asgi:asgi3                       RUNNING   pid 15335, uptime 1:42:43
celery-flower                    RUNNING   pid 15320, uptime 1:42:45
celery-worker                    RUNNING   pid 15321, uptime 1:42:45
xops                             RUNNING   pid 15328, uptime 1:42:44
[root@xuxu xufeng]# supervisorctl status
```

生成前端页面

配置nginx

```
upstream xops {
   server 127.0.0.1:8000;
}
upstream channels-backend {
   server 127.0.0.1:8001;
}

server {
    listen      80;
    server_name demo.xufqing.cn;#你的访问地址,和前端生产的地址一致
    location / {
        try_files $uri $uri/ /index.html;
        add_header access-control-allow-origin *;
        root /home/xufeng/rest_xops/xops_web;
    }
    location ^~/api  {
	uwsgi_pass xops;
        include uwsgi_params;
    }
    location ^~/auth  {
        uwsgi_pass xops;
        include uwsgi_params;
    }
    location ^~/media  {
        alias /home/xufeng/rest_xops/media;
    }
    location ^~/websocket/console {
        try_files $uri @proxy_to_app;
    }
    location @proxy_to_app {
        proxy_pass http://channels-backend;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }
}
```


最后 http://demo.xufqing.cn（你的地址）登陆访问



