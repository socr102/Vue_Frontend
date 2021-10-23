from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('stores/', views.StoreList.as_view()),
    path('stores/<int:pk>/', views.StoreDetail.as_view({'get': 'retrieve', 'update': 'update', })),
    path('orders/', views.OrderList.as_view()),
    path('articles/', views.ArticleList.as_view()),
    path('articles/rec/', views.ArticleRecommendations.as_view()),
    path('articles/connected/', views.ConnectedArticles.as_view()),
    path('articles/bought_together/', views.BoughtTogetherArticles.as_view()),
    path('payments/', views.PaymentList.as_view()),
    path('products/', views.ProductList.as_view()),
    path('products/connected/', views.ConnectedProducts.as_view()),
    path('products/rec/', views.ProductRecommendations.as_view()),
    path('receipts/<int:pk>/', views.ReceiptOrdersList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
