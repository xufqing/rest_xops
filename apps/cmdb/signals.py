# @Time    : 2019/2/17 0:56
# @Author  : xufqing
import os

from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import DeviceFile


@receiver(post_delete, sender=DeviceFile)
def auto_delete_file(sender, instance, **kwargs):
    if instance.file_content:
        if os.path.isfile(instance.file_content.path):
            os.remove(instance.file_content.path)