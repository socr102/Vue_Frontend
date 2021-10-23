from django.urls import path

from .views import OrgViewSet

urlpatterns = [
    path('orgs/', OrgViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('orgs/<int:pk>/', OrgViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }))
]
