from rest_framework import serializers
from portrait.models import CartoonImage



class UpdateFAQSerializer(serializers.Serializer):
    question = serializers.CharField(required=False, allow_blank=True)
    answer = serializers.CharField(required=False, allow_blank=True)
    is_featured = serializers.BooleanField()




class AddFAQSerializer(serializers.Serializer):
    question = serializers.CharField(required=True)
    answer = serializers.CharField(required=True)
    is_featured = serializers.BooleanField(required=True)





class PurchaseUpdateSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)



class PortraitUploadSerialiser(serializers.ModelSerializer):

    class Meta:
        model = CartoonImage
        fields = "__all__"



# class UpdatePortraitSerialiser(serializers.Serializer):
#     description = serializers.CharField(required=False)
#     price = serializers.DecimalField(required=False)
#     is_featured = serializers.BooleanField(allow_null=True)
#     image = serializers.ImageField(allow_null=True)


