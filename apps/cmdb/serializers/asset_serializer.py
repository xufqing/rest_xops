# @Time    : 2019/2/21 16:20
# @Author  : xufqing
from rest_framework import serializers
from ..models import DeviceInfo

class DeviceInfoSerializer(serializers.ModelSerializer):
    '''
    设备信息序列化
    '''
    class Meta:
        model = DeviceInfo
        fields = '__all__'

class DeviceInfoListSerializer(serializers.ModelSerializer):
    '''
    设备列表序列化
    '''
    class Meta:
        model = DeviceInfo
        fields = ('id','sys_hostname','hostname','auth_type','os_version','status')

class DeviceListSerializer(serializers.Serializer):
    key = serializers.CharField(source='id')
    label = serializers.CharField(source='hostname')