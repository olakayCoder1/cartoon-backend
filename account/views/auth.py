from threading import Thread
from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status  , generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied , NotAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import User 
from account.mixins import PublicApiMixin, ApiErrorsMixin
from account.utils import google_get_access_token, google_get_user_info
from account.serializer import (
    ResetPasswordRequestEmailSerializer,
    ChangePasswordSerializer , 
    SetNewPasswordSerializer , 
    LoginSerializer,SignupSerializer
)
from helpers.mail import MailServices
from helpers.tokens import create_jwt_pair_for_user




def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token


class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}/login'
    
        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_FRONTEND_URL}/google'
        access_token = google_get_access_token(code=code, 
                                               redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        try:
            user = User.objects.get(email=user_data['email'])
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': user.serialized_user_data(),
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data)
        except User.DoesNotExist:
            # username = user_data['email'].split('@')[0]
            first_name = user_data.get('given_name', '')
            last_name = user_data.get('family_name', '')

            user = User.objects.create(
                # username=username,
                email=user_data['email'],
                first_name=first_name,
                last_name=last_name,
                is_google=True,
            )
         
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': user.serialized_user_data(),
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data)



class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
  
  
    def post(self, request ):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True): 
            email = serializer.validated_data['email'] 
            password = serializer.validated_data['password']
            user = authenticate(email=email , password=password)
            

            mail = User.check_email(email)
            print(user)
            print(mail.__dict__)
            if user is not None :
                if user.is_active:
                    serializer = User.objects.get(pk=user.id)
                    print(serializer)
                    tokens = create_jwt_pair_for_user(user)
                    response = {
                        'status': True ,
                        'detail': 'Login is successful',
                        "tokens" : tokens , 
                        'user' : serializer.serialized_user_data() 
                    }
                    return Response(response , status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied(
                        "Your account is disabled, kindly contact the administrative")
            if mail and mail.is_google:
                return Response( dict(status=False,detail="Please log in with Google instead.")
                    ,status=status.HTTP_403_FORBIDDEN)
            return Response({'status': False , 'detail': 'Invalid login credential'}, status=status.HTTP_400_BAD_REQUEST)




class SignUpApiView(generics.GenericAPIView):
    serializer_class = SignupSerializer
  
  
    def post(self, request ):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True): 
            email = serializer.validated_data['email'] 
            password = serializer.validated_data['password']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']

            mail = User.check_email(email)

            if mail:
                return Response(dict(status=False,detail="Email already exist"),status=status.HTTP_400_BAD_REQUEST)
            
            new_obj = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email.lower()
            )

            new_obj.set_password(password)
            new_obj.save()
            tokens = create_jwt_pair_for_user(new_obj)
            response = {
                'status': True ,
                'detail': 'Reistration is successful',
                "tokens" : tokens , 
                'user' : new_obj.serialized_user_data() 
            }
            return Response(response , status=status.HTTP_200_OK)



class ResetPasswordRequestEmailApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestEmailSerializer
    


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = request.data['email']
            try:
                user = User.objects.get(email=email)
                uuidb64 = urlsafe_base64_encode(force_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                Thread(target=MailServices.forget_password_mail, kwargs={
                    'email': user.email ,'token': token , 'uuidb64':uuidb64
                }).start()
                return Response( 
                        {'status':True , 'detail': 'Password reset instruction will be sent to the mail' },
                        status=status.HTTP_200_OK
                        )
            except:
                return Response( 
                    {'status':True , 'detail': 'Password reset instruction will be sent to the mail' }, 
                    status=status.HTTP_200_OK
                    )
        return Response( 
                    {'status':False , 'detail': 'Enter a valid email address' }, 
                    status=status.HTTP_400_BAD_REQUEST
                    )

# This view handle changing of user password on forget password
class SetNewPasswordTokenCheckApi(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer



    def post(self, request, token , uuidb64 ):
        try:
            id = smart_str(urlsafe_base64_decode(uuidb64))
            user = User.objects.get(id=id)
            password1 = request.data['password1']
            password2 = request.data['password2']
            if password1 != password2 :
                return  Response({'status':False ,'detail': 'Password does not match'} , status=status.HTTP_400_BAD_REQUEST)
            if PasswordResetTokenGenerator().check_token(user, token):
                data = request.data
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                user.set_password(serializer.validated_data['password1'])
                user.save() 
                return Response({'status':True , 'detail':'Password updated successfully'}, status=status.HTTP_200_OK)
            return Response({'status':False ,'detail':'Token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        except DjangoUnicodeDecodeError as identifier:
            return Response({'status':False ,'detail': 'Token is not valid'}, status=status.HTTP_400_BAD_REQUEST)


#  This view handle password update within app ( authenticated user)
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer 
    permission_classes = [ IsAuthenticated ] 
    model = User

    def get_object(self,queryset=None):
        obj = self.request.user
        return obj
    


    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            password1 = serializer.validated_data['password1']
            password2 = serializer.validated_data['password2']
            if password1 != password2 :
                return  Response({'status':False ,'detail': 'Password does not match'} , status=status.HTTP_400_BAD_REQUEST)
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'status':False ,'detail': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("password2"))
            self.object.save()
            response={
                'status': True,
                'detail': 'Password updated successfully',
                }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


