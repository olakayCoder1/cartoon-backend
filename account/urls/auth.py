from django.urls import path , include
from account.views.auth import *


urlpatterns = [
    path('login', LoginApiView.as_view() ),
    path('register', SignUpApiView.as_view() ),
    path('forget-password', ResetPasswordRequestEmailApiView.as_view() ),
    path('set-password', SetNewPasswordTokenCheckApi.as_view() ),
    path('change-password', ChangePasswordView.as_view() ),
    path("login/google/", GoogleLoginApi.as_view(), name="login-with-google"),
]