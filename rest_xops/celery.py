from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_xops.settings') # 设置django环境

app = Celery('rest_xops')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks() # 自动发现task，这个配置会自动从每个app目录下去发现tasks.py文件

# 以下内容也可以写在settings.py文件中


BROKER_URL = 'redis://localhost:16379/1' # Broker配置，使用Redis作为消息中间件

CELERY_RESULT_BACKEND = 'redis://localhost:16379/1' # Backend设置，使用redis作为后端结果存储

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_ENABLE_UTC = False

CELERYD_FORCE_EXECV = True # 防止任务死锁

CELERYD_CONCURRENCY = 8 # 并发的worker数量

CELERY_ACKS_LATE = True

CELERYD_MAX_TASKS_PER_CHILD = 100 # 每个worker最多执行的任务数

CELERYD_TASK_TIME_LIMIT = 15 * 60 # 任务超时时间