# @Time    : 2019/4/24 13:00
# @Author  : xufqing
from rest_framework import serializers
from ..models import DeviceGroup
from ..models import DeviceInfo


class DeviceGroupSerializer(serializers.ModelSerializer):
    '''
    主机组序列化
    '''
    hosts = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=DeviceInfo.objects.all(), source='deviceinfo_set')
    class Meta:
        model = DeviceGroup
        fields = '__all__'