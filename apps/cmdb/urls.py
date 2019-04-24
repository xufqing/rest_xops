from django.urls import path,include
from cmdb.views import dict,scan,asset,connection,business,group,label
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'dicts', dict.DictViewSet, base_name="dicts")
router.register(r'scan/devices', scan.DeviceScanInfoViewSet, base_name="scan_devices")
router.register(r'devices', asset.DeviceInfoViewSet, base_name="devices")
router.register(r'connections', connection.ConnectionInfoViewSet, base_name="connections")
router.register(r'businesses', business.BusinessViewSet, base_name="businesses")
router.register(r'groups', group.DeviceGroupViewSet, base_name="groups")
router.register(r'labels', label.LabelViewSet, base_name="labels")

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/dict/tree/', dict.DictTreeView.as_view(), name='dict_tree'),
    path(r'api/scan/setting/', scan.ScanSettingView.as_view(), name='scan_setting'),
    path(r'api/scan/excu/', scan.ScanExcuView.as_view(), name='scan_excu'),
    path(r'api/device/list/', asset.DeviceListView.as_view(), name='device_list'),
]
