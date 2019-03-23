from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path(r'', include('rbac.urls')),
    path(r'', include('cmdb.urls')),
    path(r'', include('deployment.urls')),
    path('docs/', include_docs_urls()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
