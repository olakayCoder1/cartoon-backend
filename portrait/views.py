from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from portrait.models import CartoonImage , CustomImage , FavouriteImage , CartoonImageUserFavourite , CartoonImageUserLike , PurchaseImage
from .serializers import AllPortraitSerializer , LikePortraitSerializer ,PurchasePortraitSerializer
from helpers.pagination import Paginator
from helpers.data_process import encrypt_data , decrypt_data
from account.models import User
# Create your views here.

import json
from decimal import Decimal





class GetAllFeaturedCustomImagesApiView(APIView):
    def get(self, request):
        records = [ dict(
                id=val.id,
                image=val.image.url,
                description=val.description,
                price=float(val.price),
                likes_count=val.likes_count,
                saves_count=val.saves_count,
                comments_count=val.comments_count,
                ) for val in CartoonImage.objects.filter(is_featured=True)]
        return Response(dict(status=True,data=records),status=status.HTTP_200_OK)
    


class GetUserSavedImageApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        records = FavouriteImage.get_user_favourites(request.user.id)
        return Response(dict(status=True,data=records),status=status.HTTP_200_OK)
    


class GetAllCustomImagesApiView(APIView,Paginator):

    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        page_size = int(request.GET.get("page_size",20))
        # data = encrypt_data(CartoonImage.get_all_images(request))
        # self.records = data
        self.records = CartoonImage.get_all_images(request)
        return self.paginate(page_size) if page_size else self.paginate(100)

    

    def post(self, request):
        data = request.data.get('key')
        real_data = decrypt_data(data)
        return Response(eval(real_data), status=status.HTTP_200_OK)
    

class GetPortraitDetails(APIView):

    def get(self, request, portrait_id):
        try:
            val = CartoonImage.objects.filter(uuid=portrait_id).first()
            if not val:
                return Response(dict(statu=False, detail='Record not found'), status=status.HTTP_404_NOT_FOUND)
            
            full_image_url = request.build_absolute_uri(val.image.url)
            data = dict(
                id=val.id,
                image=full_image_url,
                description=val.description,
                price=val.price,
                likes_count=val.likes_count,
                saves_count=val.saves_count,
                comments_count=val.comments_count,
            )
            return Response(dict(status=True,data=data),status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(dict(statu=False, detail='Record not found'), status=status.HTTP_404_NOT_FOUND)
        


class GetAddLikePortrait(APIView,Paginator):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        page_size = int(request.GET.get("page_size",20))
        data = CartoonImageUserLike.get_user_likes(request.user.id)
        self.records = data
        return self.paginate(page_size)



    def post(self, request):
        serializer = LikePortraitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            val = CartoonImage.objects.filter(uuid=serializer.validated_data['portrait_id']).first()
            if not val:
                return Response(dict(statu=False, detail='Record not found'), status=status.HTTP_404_NOT_FOUND)
            
            user = User.objects.get(pk=request.user.id)
            has_already_liked = CartoonImageUserLike.objects.filter(user=user, portrait=val).first()
            if not has_already_liked:
                CartoonImageUserLike.objects.create(user=user, portrait=val)
                prev = val.likes_count 
                val.likes_count = prev + 1
                val.save()
            return Response(dict(status=True),status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(dict(statu=False, detail='An error occured'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetAddSavePortrait(APIView,Paginator):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        page_size = int(request.GET.get("page_size",20))
        data = CartoonImageUserFavourite.get_user_favourites(request.user.id)
        self.records = data
        return self.paginate(page_size)

    def post(self, request):
        serializer = LikePortraitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            val = CartoonImage.objects.get(pk=serializer.validated_data['portrait_id'])
            user = User.objects.get(request.user.id)
            has_already_liked = FavouriteImage.objects.filter(user=user, portrait=val)
            if not has_already_liked:
                FavouriteImage.objects.create(user=user, portrait=val)
                prev= val.saves_count 
                val.saves_count = prev + 1
                val.save()
            return Response(dict(status=True),status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(dict(statu=False, detail='Record not found'), status=status.HTTP_404_NOT_FOUND)





class PurchasePortrait(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serialiser = PurchasePortraitSerializer(data=request.data)
        serialiser.is_valid(raise_exception=True)
        user = User.objects.get(pk=request.user.id)
        try:
            portrait = CartoonImage.objects.filter(uuid=serialiser.validated_data['portrait_id']).first()
            purchase = PurchaseImage.objects.create(user=user,image=portrait,price=portrait.price)
            return Response(dict(status=True,data=purchase.serialized_user_data()),status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(dict(statu=False, detail='Record not found'), status=status.HTTP_404_NOT_FOUND)