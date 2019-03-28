# @Time    : 2019/1/12 21:03
# @Author  : xufqing
from ..models import UserProfile, Menu
from ..serializers.user_serializer import UserListSerializer, UserCreateSerializer, UserModifySerializer
from ..serializers.menu_serializer import MenuSerializer
from common.custom import CommonPagination, RbacPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from rest_xops.settings import SECRET_KEY
from rest_framework import status
from operator import itemgetter
import jwt

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserAuthView(APIView):
    '''
    用户认证获取token
    '''

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            return Response({'token': jwt.encode(payload, SECRET_KEY)})
        else:
            return Response(
                {'code': '400',
                 'detail': '用户名或密码错误！'
                 }, status=status.HTTP_400_BAD_REQUEST
            )


class UserInfoView(APIView):
    '''
    获取当前用户信息和权限
    '''

    @classmethod
    def get_permission_from_role(self, request):
        try:
            if request.user:
                perms_list = []
                for item in request.user.roles.values('permissions__method').distinct():
                    perms_list.append(item['permissions__method'])
                return perms_list
        except AttributeError:
            return None

    def get(self, request):
        if request.user.id is not None:
            perms = self.get_permission_from_role(request)
            data = {
                'username': request._user.username,
                'avatar': request._request._current_scheme_host + '/media/' + str(request._user.image),
                'email': request._user.email,
                'is_active': request._user.is_active,
                'roles': perms
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({
                'code': '403',
                'detail': '请登录后访问'
            }, status=status.HTTP_403_FORBIDDEN)

class UserBuildMenuView(APIView):
    '''
    绑定当前用户菜单信息
    '''
    def get_menu_from_role(self, request):
        if request.user:
            menu_dict = {}
            menus = request.user.roles.values(
                'menus__id',
                'menus__name',
                'menus__path',
                'menus__is_frame',
                'menus__is_show',
                'menus__component',
                'menus__icon',
                'menus__sort',
                'menus__pid'
            ).distinct()
            for item in menus:
                if item['menus__pid'] is None:
                    if item['menus__is_frame']:
                        # 判断是否外部链接
                        top_menu = {
                            'id': item['menus__id'],
                            'path': item['menus__path'],
                            'component': 'Layout',
                            'children': [{
                                'path': item['menus__path'],
                                'meta': {
                                    'title': item['menus__name'],
                                    'icon': item['menus__icon']
                                }
                            }],
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    else:
                        top_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': '/' + item['menus__path'],
                            'redirect': 'noredirect',
                            'component': 'Layout',
                            'alwaysShow': True,
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon']
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort'],
                            'children': []
                        }
                    menu_dict[item['menus__id']] = top_menu
                else:
                    if item['menus__is_frame']:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': 'Layout',
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon'],
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    elif item['menus__is_show']:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': item['menus__component'],
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon'],
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    else:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': item['menus__component'],
                            'meta': {
                                'title': item['menus__name'],
                                'noCache': True,
                            },
                            'hidden': True,
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    menu_dict[item['menus__id']] = children_menu
            return menu_dict

    def get_all_menu_dict(self):
        '''
        获取所有菜单数据，重组结构
        '''
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        tree_dict = {}
        for item in serializer.data:
            if item['pid'] is None:
                if item['is_frame']:
                    # 判断是否外部链接
                    top_menu = {
                        'id': item['id'],
                        'path': item['path'],
                        'component': 'Layout',
                        'children': [{
                            'path': item['path'],
                            'meta': {
                                'title': item['name'],
                                'icon': item['icon']
                            }
                        }],
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    top_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': '/' + item['path'],
                        'redirect': 'noredirect',
                        'component': 'Layout',
                        'alwaysShow': True,
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon']
                        },
                        'pid': item['pid'],
                        'sort': item['sort'],
                        'children': []
                    }
                tree_dict[item['id']] = top_menu
            else:
                if item['is_frame']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': 'Layout',
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                elif item['is_show']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'noCache': True,
                        },
                        'hidden': True,
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                tree_dict[item['id']] = children_menu
        return tree_dict

    def get_all_menus(self, request):
        perms = UserInfoView.get_permission_from_role(request)
        tree_data = []
        if 'admin' in perms or request.user.is_superuser:
            tree_dict = self.get_all_menu_dict()
        else:
            tree_dict = self.get_menu_from_role(request)
        for i in tree_dict:
            if tree_dict[i]['pid']:
                pid = tree_dict[i]['pid']
                parent = tree_dict[pid]
                parent.setdefault('redirect', 'noredirect')
                parent.setdefault('alwaysShow', True)
                parent.setdefault('children', []).append(tree_dict[i])
                parent['children'] = sorted(parent['children'], key=itemgetter('sort'))
            else:
                tree_data.append(tree_dict[i])
        return tree_data

    def get(self, request):
        if request.user.id is not None:
            menu_data = self.get_all_menus(request)
            return Response(sorted(menu_data, key=itemgetter('sort')), status=status.HTTP_200_OK)
        else:
            return Response({
                'code': '403',
                'detail': '请登录后访问'
            }, status=status.HTTP_403_FORBIDDEN)


class UserViewSet(ModelViewSet):
    '''
    用户管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'user_all'}, {'get': 'user_list'}, {'post': 'user_create'}, {'put': 'user_edit'},
                 {'delete': 'user_delete'})
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('is_active',)
    search_fields = ('username', 'name', 'mobile', 'email')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserModifySerializer

    def create(self, request, *args, **kwargs):
        # 创建用户默认添加密码
        request.data['password'] = '123456'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
