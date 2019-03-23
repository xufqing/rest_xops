# @Time    : 2019/2/27 10:42
# @Author  : xufqing
from rest_framework import serializers
from ..models import Business

class BusinessSerializer(serializers.ModelSerializer):
    '''
    业务序列化
    '''
    class Meta:
        model = Business
        fields = '__all__'

class BusinessTreeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')
    pid = serializers.PrimaryKeyRelatedField(read_only=True)