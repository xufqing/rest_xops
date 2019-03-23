# @Time    : 2019/1/14 18:08
# @Author  : xufqing
from rest_framework import serializers
from ..models import Menu


class MenuSerializer(serializers.ModelSerializer):
    '''
    菜单序列化
    '''

    class Meta:
        model = Menu
        fields = ('id', 'name', 'icon', 'path', 'is_show','is_frame', 'sort', 'component', 'pid')
        extra_kwargs = {'name': {'required': True, 'error_messages': {'required': '必须填写菜单名'}}}
