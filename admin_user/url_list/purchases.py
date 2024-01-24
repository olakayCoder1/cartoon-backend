from django.urls import path , include
from admin_user.views.purchases import *


urlpatterns = [
    path('', AllPurchases.as_view() ),
    path('add', AllPurchases.as_view() ),
    path('<purchase_id>', GetUpdateDeletePurchase.as_view() ),
]