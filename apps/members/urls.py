from django.urls import path

from .views import (MembersList, MemberDetail,
                    MemberReceiptsList,
                    MemberCampaignsList,
                    MemberCampaignDetail)

urlpatterns = [
    path('members/', MembersList.as_view()),
    path('members/<int:pk>/', MemberDetail.as_view()),
    path('members/<int:pk>/receipts/', MemberReceiptsList.as_view()),
    path('members/<int:pk>/campaigns/', MemberCampaignsList.as_view()),
    path('members/<int:pk>/campaigns/<int:campaign_id>/orders/',
         MemberCampaignDetail.as_view()),
]
