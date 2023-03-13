from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('network/', include('network.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),

        # URLs документации.
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
    ]
