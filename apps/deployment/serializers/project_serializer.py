# @Time    : 2019/2/27 14:39
# @Author  : xufqing
from rest_framework import serializers
from ..models import Project,DeployRecord

class ProjectSerializer(serializers.ModelSerializer):
    '''
    项目序列化
    '''
    class Meta:
        model = Project
        fields = '__all__'

class ProjectListSerializer(serializers.ModelSerializer):
    '''
    项目列表序列化
    '''
    class Meta:
        model = Project
        fields = ('id', 'name', 'environment', 'status', 'alias', 'last_task_status', 'server_ids', 'user_id')

class DeployRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeployRecord
        fields = '__all__'