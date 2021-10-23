from django.urls import path

from . import views

urlpatterns = [
    path('account/', views.UserList.as_view()),
    path('account/<int:pk>/', views.UserDetail.as_view()),
    path('account/<int:pk>/password/', views.ChangePassword.as_view()),
    path('account/<int:pk>/deactivate/', views.DeactivateUser.as_view()),
]
