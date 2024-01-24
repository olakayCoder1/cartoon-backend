from rest_framework import serializers




class PaymentCheckoutSerializer(serializers.Serializer):
    purchase_id = serializers.CharField(required=True)


class PaymentCheckoutConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)



class AnonymousPaymentCheckoutSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    # image = serializers.ImageField(required=False, null=True) 
    watermark = serializers.CharField(required=True)
    note = serializers.CharField(required=False, allow_blank=True)



class UserJoinNewsletterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)