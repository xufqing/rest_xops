# @Time    : 2019/2/27 14:39
# @Author  : xufqing
from rest_framework.viewsets import ModelViewSet
from ..models import Project
from ..serializers.project_serializer import ProjectSerializer, ProjectListSerializer
from common.custom import CommonPagination, RbacPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

class ProjectViewSet(ModelViewSet):
    '''
    业务管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'project_all'}, {'get': 'project_list'}, {'post': 'project_create'}, {'put': 'project_edit'},
                 {'delete': 'project_delete'})
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('environment','status',)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer