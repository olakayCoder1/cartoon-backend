from uuid import uuid4
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from helpers.pagination import Paginator
from admin_user.models import FAQ 
from admin_user.serializers import UpdateFAQSerializer , AddFAQSerializer




class AllFAQ(APIView, Paginator ):

    def get(self, request):
        page_size = int(request.GET.get("page_size",20))
        self.records = [ val.serialized_user_data() for val in FAQ.objects.all().order_by('-created_at')]
        return self.paginate(page_size) if page_size else self.paginate(20)
    


    def post(self, request):
        serialiser = AddFAQSerializer(data=request.data)
        serialiser.is_valid(raise_exception=True)
        unique_uuid = str(uuid4())
        try:
            record = FAQ.objects.create(
                uuid=unique_uuid, 
                question=request.data['question'],
                answer=request.data['answer'],
                is_featured=request.data['is_featured']
            )
            return Response(dict(
                    status=True,
                    detail='Record successfully saved',
                    data=record.serialized_user_data()
                    ),status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(dict(status=False,detail='An error occured saving record' ),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
       




class GetUpdateDeleteFAQ(APIView ):

    def get(self, request, faq_id):
        try:
            record = FAQ.objects.filter(uuid=faq_id).first()
            return Response(dict(status=False,data=record.serialized_user_data()),status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(dict(status=False,detail='Record not found'),status=status.HTTP_404_NOT_FOUND)
        
    
    def put(self, request, faq_id):
        serialiser = UpdateFAQSerializer(data=request.data)
        serialiser.is_valid(raise_exception=True)
        try:
            record = FAQ.objects.filter(uuid=faq_id).first()
            record.answer = request.data['answer'] if request.data.get('answer',None) else record.answer
            record.question = request.data['question'] if request.data.get('question',None) else record.question
            record.is_featured = request.data['is_featured'] if request.data.get('is_featured',None) else record.is_featured
            record.save()
            return Response(dict(status=True,detail='Record successfully updated',
                data=record.serialized_user_data()),status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response(dict(status=False,detail='Record not found'),status=status.HTTP_404_NOT_FOUND)
        
        

    def delete(self, request, faq_id):
        try:
            record = FAQ.objects.filter(uuid=faq_id).first()
            record.delete()
            return Response(dict(status=True,detail='Record successfully deleted'),status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response(dict(status=False,detail='Record not found'),status=status.HTTP_404_NOT_FOUND)


