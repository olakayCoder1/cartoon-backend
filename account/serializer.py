from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)




class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)
    email = serializers.EmailField(allow_blank=False)
    # phone = serializers.CharField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)




class ResetPasswordRequestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    redirect_url = serializers.CharField(required=True)
    class Meta:
        fields =  ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=6,max_length=30, required=True )
    password2 = serializers.CharField(min_length=6,max_length=30, required=True )
    
    class Meta:
        fields = ['password', 'password2']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True )
    password1 = serializers.CharField(required=True )
    password2 = serializers.CharField(required=True )