from django.urls import path , include
from admin_user.views.portraits import *


urlpatterns = [
    path('', CartoonImageUploadApiView.as_view()),
    path('<uuid>', GetUpdateDeleteDeleteCartoonImageUploadApiView.as_view()) 
]