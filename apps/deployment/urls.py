# @Time    : 2019/2/27 14:42
# @Author  : xufqing
from django.urls import path,include
from deployment.views import project, deploy, applog
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'projects', project.ProjectViewSet, base_name="projects")
router.register(r'deploy/records', deploy.DeployRecordViewSet, base_name="deploy_record")
urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/deploy/excu/', deploy.DeployView.as_view(), name='deploy'),
    path(r'api/deploy/ver/', deploy.VersionView.as_view(), name='version'),
    path(r'api/deploy/applog/', applog.AppLogView.as_view(), name='applog'),
    path(r'api/project/copy/', project.ProjectCopy.as_view(), name='project_copy')
]