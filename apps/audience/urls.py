from django.urls import path

from .views import AudienceList, AudienceDetail

urlpatterns = [
    path('audience/', AudienceList.as_view()),
    path('audience/<int:pk>/', AudienceDetail.as_view())
]
