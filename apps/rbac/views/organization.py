# @Time    : 2019/1/12 21:03
# @Author  : xufqing
from rest_framework.viewsets import ModelViewSet
from ..models import Organization
from ..serializers.organization_serializer import OrganizationSerializer, OrganizationUserTreeSerializer
from common.custom import CommonPagination, RbacPermission, TreeAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView
from rest_xops.basic import XopsResponse
from rest_framework.permissions import IsAuthenticated


class OrganizationViewSet(ModelViewSet, TreeAPIView):
    '''
    组织机构：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'organization_all'}, {'get': 'organization_list'}, {'post': 'organization_create'},
    {'put': 'organization_edit'},{'delete': 'organization_delete'})
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)


class OrganizationTreeView(TreeAPIView):
    '''
    组织架构树
    '''
    queryset = Organization.objects.all()


class OrganizationUserTreeView(APIView):
    '''
    组织架构关联用户树
    '''
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        organizations = Organization.objects.all()
        serializer = OrganizationUserTreeSerializer(organizations, many=True)
        tree_dict = {}
        tree_data = []
        for item in serializer.data:
            new_item = {
                'id': 'o' + str(item['id']),
                'label': item['label'],
                'pid': item['pid'],
                'children': item['children']
            }
            tree_dict[item['id']] = new_item
        for i in tree_dict:
            if tree_dict[i]['pid']:
                pid = tree_dict[i]['pid']
                parent = tree_dict[pid]
                parent['children'].append(tree_dict[i])
            else:
                tree_data.append(tree_dict[i])
        return XopsResponse(tree_data)
