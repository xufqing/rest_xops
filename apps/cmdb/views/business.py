# @Time    : 2019/2/27 10:42
# @Author  : xufqing
from rest_framework.viewsets import ModelViewSet
from ..models import Business
from ..serializers.business_serializer import BusinessSerializer,BusinessTreeSerializer
from common.custom import CommonPagination, RbacPermission, TreeAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class BusinessViewSet(ModelViewSet, TreeAPIView):
    '''
    业务管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'business_all'}, {'get': 'business_list'}, {'post': 'business_create'}, {'put': 'business_edit'},
                 {'delete': 'business_delete'})
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)



class BusinessTreeView(TreeAPIView):
    '''
    业务树
    '''
    queryset = Business.objects.all()
    serializer_class = BusinessTreeSerializer