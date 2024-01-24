from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from helpers.pagination import Paginator
from account.models import User , NewsLetterUser
from portrait.models import PurchaseImage 




class AllUsers(APIView, Paginator ):

    def get(self, request):
        page_size = int(request.GET.get("page_size",20))
        self.records = [ val.serialized_user_data() for val in User.objects.filter(is_admin= False).order_by('-created_at')]
        return self.paginate(page_size) if page_size else self.paginate(100)




class GetUser(APIView ):

    def get(self, request, user_id):
        try:
            user = User.objects.filter(uuid=user_id).first()
            return Response(dict(status=True,data=user.serialized_user_data()),status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(dict(status=False,detail='Record not found'),status=status.HTTP_404_NOT_FOUND)




class GetAllNewsLetterUsers(APIView , Paginator):

    def get(self, request):
        page_size = int(request.GET.get("page_size",20))
        self.records = [ dict(id=val.uuid,email=val.email ) for val in NewsLetterUser.objects.all()]
        return self.paginate(page_size) if page_size else self.paginate(100)




class GetUserPurchase(APIView, Paginator):

    def get(self, request, user_id):
        page_size = int(request.GET.get("page_size",20))
        self.records = [ val.serialized_user_data() for val in PurchaseImage.objects.filter(user__uuid=user_id)]
        return self.paginate(page_size) if page_size else self.paginate(100)


