# @Time    : 2019/2/21 13:02
# @Author  : xufqing
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from ..serializers.asset_serializer import DeviceInfoSerializer, DeviceInfoListSerializer, DeviceListSerializer
from common.custom import CommonPagination, RbacPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models import DeviceInfo
from deployment.models import Project
from rest_xops.basic import XopsResponse
from rest_xops.code import *
from django.db.models import Q


class DeviceInfoViewSet(ModelViewSet):
    '''
    字典管理：增删改查
    '''
    perms_map = (
        {'*': 'admin'}, {'*': 'device_all'}, {'get': 'device_list'}, {'post': 'device_create'}, {'put': 'device_edit'},
        {'delete': 'device_delete'}, {'get': 'group_list'})
    queryset = DeviceInfo.objects.all()
    serializer_class = DeviceInfoSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('status','os_type', 'device_type', 'groups', 'businesses', 'labels')
    search_fields = ('hostname', 'os_type')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'list':
            return DeviceInfoListSerializer
        return DeviceInfoSerializer

    def destroy(self, request, *args, **kwargs):
        # 删除其他关联资产的数据
        instance = self.get_object()
        id = str(kwargs['pk'])
        projects = Project.objects.filter(
            Q(server_ids__icontains=id + ',') | Q(server_ids__in=id) | Q(server_ids__endswith=',' + id)).values()
        if projects:
            for project in projects:
                server_ids = project['server_ids'].split(',')
                server_ids.remove(id)
                server_ids = ','.join(server_ids)
                Project.objects.filter(id=project['id']).update(server_ids=server_ids)
        self.perform_destroy(instance)

        return XopsResponse(status=NO_CONTENT)


class DeviceListView(ListAPIView):
    queryset = DeviceInfo.objects.all()
    serializer_class = DeviceListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('os_type',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
