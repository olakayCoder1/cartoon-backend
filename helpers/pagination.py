from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'metadata': {
                'count': self.page.paginator.count,
                'page_size': self.page_size,
                'page': self.page.number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'results': data
        })

class Paginator:
    paginator = CustomPagination()

    def __init__(self, records, request):
        """
        Method that paginate all the records
        """
        self.records = records 
        self.request = request

    def paginate(self, no_of_record: int):
        print(no_of_record)
        self.paginator.page_size = no_of_record
        result_page = self.paginator.paginate_queryset(self.records, self.request)
        return self.paginator.get_paginated_response(result_page)
