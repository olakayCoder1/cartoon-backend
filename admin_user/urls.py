from django.urls import path , include
from admin_user.views.faq import *


urlpatterns = [
    path('users/', include('admin_user.url_list.users') ),
    path('purchases/', include('admin_user.url_list.purchases') ),
    path('portraits/', include('admin_user.url_list.portraits') ),
    path('portraits', include('admin_user.url_list.portraits') ),
    path('faq', AllFAQ.as_view() ),
    path('faq/<faq_id>', GetUpdateDeleteFAQ.as_view() ),
]