# @Time    : 2019/3/13 10:51
# @Author  : xufqing
import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest_xops.settings")
django.setup()
application = get_default_application()