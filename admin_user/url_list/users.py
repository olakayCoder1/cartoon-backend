from django.urls import path , include
from admin_user.views.users import *


urlpatterns = [
    path('', AllUsers.as_view() ),
    path('newsletter', GetAllNewsLetterUsers.as_view() ),
    path('<user_id>', GetUser.as_view() ),
    path('<user_id>/purchase', GetUserPurchase.as_view() ),
]