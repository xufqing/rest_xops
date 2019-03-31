demo地址: http://demo.xufqing.cn

管理员账号:admin 密码admin@1234

![1.png](https://raw.githubusercontent.com/xufqing/rest_xops/master/demo/1.png)

![2.png](https://raw.githubusercontent.com/xufqing/rest_xops/master/demo/2.png)

![3.png](https://raw.githubusercontent.com/xufqing/rest_xops/master/demo/3.png)

![4.png](https://raw.githubusercontent.com/xufqing/rest_xops/master/demo/4.png)

***特色功能开发进度***

- 已完成
- [X] 基于RBAC的用户权限管理
- [X] 资产扫描功能（目前只能扫描linux服务器）
- [X] 持续构建（websocket实时显示过程）
- [X] 项目应用控制（启动停止）
- [X] 应用日志的实时查看（websocket）
- [X] 对象级权限控制（密码管理功能，只能查看编辑自己的密码）
- 待开发
- [ ] 工单系统
- [ ] 作业平台（ansible api）
- [ ] 应用日志下载
- [ ] 文件管理
- [ ] WEBSSH（堡垒机）
- [ ] SQL作业平台
- ...........

***本项目采用以下技术***

前端：

vue 2.5.17

elementUI 2.6.0

websocket

后端：

django 2.1.4

django rest framework 3.9.1

django rest framework-jwt 1.11.0

django channels 2.1.7

celery 4.2.1

软件运行环境

Python 3.6.8

Redis 5.0

MySql 5.7

***基础环境安装***

1、安装npm运行环境(略)

    安装前端项目依赖包
    
    cd xops_qd_source/
    npm install

2、修改你的配置文件

    xops_qd_source/config

    dev.env.js #开发环境

    prod.env.js #生成环境

3、安装mysql（略）

4、安装redis（略）

5、创建python虚拟环境

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
2、安装项目运行模块
```
pip install -r requirements.txt
```
3、修改配置
```
vi rest_xops/settings.py 
# 修改数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rest_xops',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': '123456',
        'PORT': '3306',
        'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;' }
    }
}
# 修改redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

#修改redis
vi rest_xops/celery.py

BROKER_URL = 'redis://localhost:6379/1' # Broker配置，使用Redis作为消息中间件

CELERY_RESULT_BACKEND = 'redis://localhost:6379/1' # Backend设置，使用redis作为后端结果存储


```


4、登陆MYSQL，创建数据库

```
CREATE DATABASE rest_xops DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```

5、执行创建表信息

python manage.py makemigrations rbac

python manage.py makemigrations cmdb

python manage.py makemigrations deployment

python manage.py migrate

**导入初始化数据**

python manage.py loaddata init_data/*.json

如果遇到mysql模块的问题

ImportError: libmysqlclient.so.18: cannot open shared object file: No such file or directory

则：

ln -s /usr/local/mysql/lib/libmysqlclient.so.18 /usr/lib64/libmysqlclient.so.18



6、修改管理员密码（必须操作）
    
    python manage.py changepassword admin
    

7、安装扫描工具

    yum -y install nmap

8、安装进程管理

    yum -y install supervisor


9、开机启动

    systemctl enable supervisord
    systemctl start supervisord
10、配置supervisor来管理celery

- celery_worker
```
vim /etc/supervisord.d/celery_worker.ini

[program:celery-worker]
command=/home/xufeng/.pyenv/versions/rest_xops/bin/celery worker -A rest_xops -l INFO
directory=/home/xufeng/rest_xops
environment=PATH="/home/xufeng/.pyenv/versions/rest_xops/bin/"
stdout_logfile=/run/rest_xops/worker_celery.log
stderr_logfile=/run/rest_xops/worker_celery.log
autostart=true
autorestart=true
priority=901

[program:celery-flower]
command=/home/xufeng/.pyenv/versions/rest_xops/bin/celery flower --broker=redis://localhost:6379/1
directory=/home/xufeng/rest_xops
environment=PATH="/home/xufeng/.pyenv/versions/rest_xops/"
stdout_logfile=/run/rest_xops/flower_celery.log
stderr_logfile=/run/rest_xops/flower_celery.log
autostart=true
autorestart=true
priority=900


执行
supervisorctl start all

```


***开发环境的运行***

运行前端
```
cd rest_xops/xops_qd_source
npm run dev
#接下来启动后端即可进行调试
```
运行后端

    python manage.py runserver 0.0.0.0:8000
    
浏览器登陆

    http://localhost:8013/   前端
    http://你的后端地址:8000/docs/  API文档地址
    

***生产环境的运行***

**1、安装nginx（略）**

    以下所有/home/xufeng/rest_xops 都改为你的项目地址

    /home/xufeng/.pyenv/versions/rest_xops 是你的python虚拟环境的版本



**2、安装uwsgi**

```
 cd /home/xufeng/rest_xops
 
 pip install uwsgi

```
**3、设置Uwsgi配置文件**

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
**4、设置supervisord**
- xops_uwsgi
```
vim /etc/supervisord.d/xops_uwsgi.ini

[program:xops]
command=/home/xufeng/.pyenv/versions/rest_xops/bin/uwsgi /etc/xops_uwsgi.ini
stdout_logfile=/run/rest_xops/uwsgi.log
stderr_logfile=run/rest_xops/uwsgi.log
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
stdout_logfile=/run/rest_xops/asgi.log
stderr_logfile=/run/rest_xops/asgi.log
stdout_logfile_maxbytes = 20MB
```

**6、重启supervisord**

    supervisorctl reload

    systemctl restart supervisord

    supervisorctl start all

**7、查看运行状态**

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
**8、生产静态页面**
```
cd rest_xops/xops_qd_source
npm run build
```
将xops_qd_source/dist目录下生成的文件复制到你的服务器nginx web root目录

**9、配置NGINX*

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
        root /home/xufeng/rest_xops/xops_web; # 这是前端静态文件
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



