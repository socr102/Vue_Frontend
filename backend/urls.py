"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
import debug_toolbar

import backend.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.user_panel.urls')),
    path('api/v1/', include('apps.receipts.urls')),
    path('api/v1/', include('apps.trends.urls')),
    path('api/v1/', include('apps.organizations.urls')),
    path('api/v1/', include('apps.offers.urls')),
    path('api/v1/', include('apps.members.urls')),
    path('api/v1/', include('apps.audience.urls')),
    path('api/v1/', include('apps.campaigns.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += [path('debug/', include(debug_toolbar.urls))]
