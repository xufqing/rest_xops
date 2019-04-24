# @Time    : 2019/4/24 13:00
# @Author  : xufqing
from rest_framework.viewsets import ModelViewSet
from ..models import DeviceGroup
from ..serializers.group_serializer import DeviceGroupSerializer
from common.custom import CommonPagination, RbacPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class DeviceGroupViewSet(ModelViewSet):
    '''
    设备组：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'group_all'}, {'get': 'group_list'}, {'post': 'group_create'}, {'put': 'group_edit'},
                 {'delete': 'group_delete'}, {'patch': 'group_edit'})
    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)