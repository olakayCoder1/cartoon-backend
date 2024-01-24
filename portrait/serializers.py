from rest_framework import serializers
from portrait.models import CartoonImage , CustomImage



class AllPortraitSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartoonImage
        fields = '__all__'



class LikePortraitSerializer(serializers.Serializer):
    portrait_id = serializers.CharField(required=True)




class PurchasePortraitSerializer(serializers.Serializer):
    portrait_id = serializers.CharField(required=True)