# @Time    : 2019/2/15 14:35
# @Author  : xufqing

import os, logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, DestroyModelMixin,RetrieveModelMixin
from utils.common import ConfigFileMixin
from common.custom import RbacPermission, CommonPagination, CeleryTools
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ruamel import yaml
from rest_framework import status
from ..models import DeviceScanInfo,DeviceInfo,DeviceAbstract,ConnectionAbstract,ConnectionInfo
from ..serializers.scan_serializer import DeviceScanInfoSerializer,DeviceScanListSerializer
from ..tasks import scan_execution

error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class ScanSettingView(APIView, ConfigFileMixin):
    '''
    扫描设置
    '''
    perms_map = ({'*': 'admin'}, {'*': 'asset_all'})
    config_file = os.path.join(settings.YML_CONF_DIR, 'scan_settings.yml')
    permission_classes = (RbacPermission,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, format=None):
        return Response(self.get_conf_content())

    def post(self, request, format=None):
        post_data = request.data
        config = dict()
        try:
            config['net_address'] = post_data['net_address'].split(',')
            config['ssh_username'] = post_data['ssh_username']
            config['ssh_port'] = post_data['ssh_port']
            config['ssh_password'] = post_data['ssh_password']
            config['commands'] = post_data['commands']
            config['ssh_private_key'] = post_data['ssh_private_key']
            config['auth_type'] = post_data['auth_type']
            data = dict(hosts=config)
            config_file = self.get_config_file()
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, Dumper=yaml.RoundTripDumper, indent=4)
        except Exception as e:
            error_logger.error('扫描设置保存失败：' + str(e))
            return Response({'detail': '保存失败：' + str(e), }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': '保存成功', }, status=status.HTTP_200_OK)


class ScanExcuView(APIView, CeleryTools):
    '''
    设备入库和扫描
    '''
    perms_map = ({'*': 'admin'}, {'*': 'scan_all'})
    permission_classes = (RbacPermission,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, format=None):
        request_status = None
        http_status = status.HTTP_200_OK
        if request.data['excu'] == 'scan':
            celery_status = self.get_celery_worker_status()
            if celery_status:
                error_logger.error('执行失败：' + str(celery_status))
                http_status = status.HTTP_400_BAD_REQUEST
                request_status = {
                    'code':400,
                    'detail': '执行失败：' + str(celery_status),
                    }
            else:
                scan_execution.delay()
                info_logger.info('执行成功：请等待扫描结果!')
                http_status = status.HTTP_200_OK
                request_status = {
                    'code': 200,
                    'detail':'执行成功,请等待扫描结果!'
                }
        elif request.data['excu'] == 'inbound':
            login_succeed = list(DeviceScanInfo.objects.filter(status='Succeed').values())
            if login_succeed:
                device_fields = [field.name for field in DeviceAbstract._meta.fields if field.name is not 'id']
                connection_fields = [field.name for field in ConnectionAbstract._meta.fields if field.name is not 'id']
                device_fields.append('auth_type')
                for host in login_succeed:
                    device_defaults = {key: host[key] for key in host.keys() & device_fields}
                    connection_defaults = {key: host[key] for key in host.keys() & connection_fields}
                    device_defaults['changed_by_id'] = request.user.id
                    device_defaults['status'] = 'online'
                    DeviceInfo.objects.update_or_create(
                        hostname=host['hostname'],
                        defaults=device_defaults
                    )
                    ConnectionInfo.objects.update_or_create(
                        hostname=host['hostname'],
                        defaults=connection_defaults
                    )
                    DeviceScanInfo.objects.filter(hostname=host['hostname']).delete()
                http_status = status.HTTP_200_OK
                request_status = {
                    'code': 200,
                    'detail': '执行成功,' + str(len(login_succeed)) + '台设备!'
                }
            else:
                http_status = status.HTTP_400_BAD_REQUEST
                request_status = {
                    'code': 400,
                    'detail': '可入库设备为空!'
                }
        return Response(request_status,status=http_status)



class DeviceScanInfoViewSet(ListModelMixin, DestroyModelMixin,RetrieveModelMixin, GenericViewSet):
    '''
    扫描完毕的设备信息
    '''
    perms_map = ({'*': 'admin'}, {'*': 'scan_all'})
    permission_classes = (RbacPermission,)
    queryset = DeviceScanInfo.objects.all()
    serializer_class = DeviceScanInfoSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('status',)
    search_fields = ('sys_hostname', 'hostname', 'os_type')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'list':
            return DeviceScanListSerializer
        return DeviceScanInfoSerializer
