# @Time    : 2019/2/27 14:39
# @Author  : xufqing
from rest_framework.viewsets import ModelViewSet
from ..models import Project
from ..serializers.project_serializer import ProjectSerializer, ProjectListSerializer
from common.custom import CommonPagination, RbacPermission, ObjPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


class ProjectViewSet(ModelViewSet):
    '''
    业务管理：增删改查
    '''
    perms_map = (
    {'*': 'admin'}, {'*': 'project_all'}, {'get': 'project_list'}, {'post': 'project_create'}, {'put': 'project_edit'},
    {'delete': 'project_delete'})
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('environment', 'status',)
    search_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission, ObjPermission)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        '''
        只有项目组成员才能看到项目
        '''
        perms = RbacPermission.get_permission_from_role(self.request)
        if 'admin' in perms:
            return self.queryset.all()
        else:
            uid = str(self.request.user.id)
            result = self.queryset.filter(user_id__icontains=uid).filter(
                Q(user_id__icontains=uid + ',') | Q(user_id__in=uid) | Q(user_id__endswith=',' + uid))
        return result
