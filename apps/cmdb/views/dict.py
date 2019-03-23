# @Time    : 2019/2/12 16:12
# @Author  : xufqing

from rest_framework.viewsets import ModelViewSet
from ..models import Dict
from rest_framework.response import Response
from ..serializers.dict_serializer import DictSerializer, DictTreeSerializer
from common.custom import CommonPagination, RbacPermission, TreeAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class DictViewSet(ModelViewSet):
    '''
    字典管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'dict_all'}, {'get': 'dict_list'}, {'post': 'dict_create'}, {'put': 'dict_edit'},
                 {'delete': 'dict_delete'})
    queryset = Dict.objects.all()
    serializer_class = DictSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('key', 'value')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)

    def list(self, request, *args, **kwargs):
        '''
        重写list方法，即可返回树机构又可以请求参数key过滤对应的key，支持多个
        '''
        keys = self.request.query_params.get('key', '').replace(',', ' ').split()
        if not keys:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(queryset, many=True)
            tree_dict = {}
            tree_data = []
            try:
                for item in serializer.data:
                    tree_dict[item['id']] = item
                for i in tree_dict:
                    if tree_dict[i]['pid']:
                        pid = tree_dict[i]['pid']
                        parent = tree_dict[pid]
                        parent.setdefault('children', []).append(tree_dict[i])
                    else:
                        tree_data.append(tree_dict[i])
                results = tree_data
            except KeyError:
                results = serializer.data
            if page is not None:
                return self.get_paginated_response(results)
        else:
            results = []
            for key in keys:
                queryset = Dict.objects.filter(pid__key=key)
                serializer = self.get_serializer(queryset, many=True)
                results.append({key:serializer.data})
        return Response(results)



class DictTreeView(TreeAPIView):
    '''
    字典树
    '''
    queryset = Dict.objects.all()
    serializer_class = DictTreeSerializer
