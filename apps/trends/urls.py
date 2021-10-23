from django.urls import path

from . import views

urlpatterns = [
    path('trends/product/<str:direction>/', views.ProductTrends.as_view()),
    path('trends/article/<str:direction>/', views.ArticleTrends.as_view()),
]
