# @Time    : 2019/1/30 14:36
# @Author  : xufqing

from rest_framework import serializers
from ..models import Permission

class PermissionListSerializer(serializers.ModelSerializer):
    '''
    权限列表序列化
    '''
    menuname = serializers.ReadOnlyField(source='menus.name')

    class Meta:
        model = Permission
        fields = ('id','name','method','menuname','pid')