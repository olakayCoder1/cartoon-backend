from django.urls import path 
from .views import *


urlpatterns = [
    path('', GetAllCustomImagesApiView.as_view()),
    path('purchase',  PurchasePortrait.as_view()),
    path('featured', GetAllFeaturedCustomImagesApiView.as_view()),
    path('my-saves', GetUserSavedImageApiView.as_view()),
    path('likes', GetAddLikePortrait.as_view()),
    path('saves', GetAddSavePortrait.as_view()),
    path('<portrait_id>', GetPortraitDetails.as_view()),
]