# @Time    : 2019/2/24 20:38
# @Author  : xufqing
from rest_framework.viewsets import ModelViewSet
from ..serializers.connection_serializer import ConnectionInfoSerializer
from common.custom import CommonPagination, RbacPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models import ConnectionInfo

class ConnectionInfoViewSet(ModelViewSet):
    '''
    连接信息管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'connection_all'}, {'get': 'connection_list'}, {'post': 'connection_create'}, {'put': 'connection_edit'},
                 {'delete': 'connection_delete'})
    queryset = ConnectionInfo.objects.all()
    serializer_class = ConnectionInfoSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('hostname',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)