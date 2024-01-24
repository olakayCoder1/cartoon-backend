from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.generics import RetrieveUpdateDestroyAPIView 
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework.permissions import IsAuthenticated
from admin_user.serializers import PortraitUploadSerialiser 
from portrait.models import CartoonImage
from helpers.pagination import Paginator




class CartoonImageUploadApiView(APIView,Paginator ):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PortraitUploadSerialiser
    


    def get(self,request):
        page_size = int(request.GET.get("page_size",20))
        data = CartoonImage.admin_get_all_images(request)
        self.records = data
        return self.paginate(page_size)
        

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":True, "detail": "File uploaded successfully."},status=status.HTTP_201_CREATED)



class GetUpdateDeleteDeleteCartoonImageUploadApiView(RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PortraitUploadSerialiser 
    lookup_field = 'uuid'
    queryset = CartoonImage.objects.all()
    

    # def get(self,request, portrait_id):
    #     try:
    #         obj = CartoonImage.objects.get(portrait_id)
    #         return Response(dict(status=True,data=obj.serialized_data()),status=status.HTTP_200_OK)
    #     except:
    #         return Response(dict(status=False,detail="Record not found"),status=status.HTTP_404_NOT_FOUND)
        

    # def put(self,request, portrait_id):
    #     try:
    #         serialiser = UpdatePortraitSerialiser(data=request.data)
    #         serialiser.is_valid(raise_exception=True)
    #         obj = CartoonImage.objects.get(portrait_id)
    #         return Response(dict(status=True,data=obj.serialized_data()))
    #     except:
    #         return Response(dict(status=False,detail="Record not found"),status=status.HTTP_404_NOT_FOUND)
        

    # def delete(self,request, portrait_id):
    #     try:
    #         obj = CartoonImage.objects.get(portrait_id)
    #         obj.delete()
    #         return Response(dict(status=True,data='Record deleted'),status=status.HTTP_204_NO_CONTENT)
    #     except:
    #         return Response(dict(status=False,detail="Record not found"),status=status.HTTP_404_NOT_FOUND)
