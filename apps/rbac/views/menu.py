# @Time    : 2019/1/12 21:02
# @Author  : xufqing
from rest_framework.viewsets import ModelViewSet
from ..models import Menu
from ..serializers.menu_serializer import MenuSerializer
from common.custom import CommonPagination,RbacPermission,TreeAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class MenuViewSet(ModelViewSet, TreeAPIView):
    '''
    菜单管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'menu_all'}, {'get': 'menu_list'}, {'post': 'menu_create'}, {'put': 'menu_edit'},
                 {'delete': 'menu_delete'})
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('sort',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)



class MenuTreeView(TreeAPIView):
    '''
    菜单树
    '''
    queryset = Menu.objects.all()
