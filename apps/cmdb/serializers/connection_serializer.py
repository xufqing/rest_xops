# @Time    : 2019/2/24 20:36
# @Author  : xufqing
from rest_framework import serializers
from ..models import ConnectionInfo

class ConnectionInfoSerializer(serializers.ModelSerializer):
    '''
    连接密码信息序列化
    '''
    class Meta:
        model = ConnectionInfo
        fields = '__all__'