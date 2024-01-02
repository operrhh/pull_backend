from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPaginationPeopleSoft(PageNumberPagination):
    page_size = 100  # Número de elementos por página
    max_page_size = 1000  # Número máximo de elementos por página

    def get_paginated_response(self, data):
        return Response({
            'count': len(data),
            'totalResults': self.page.paginator.count,
            'hasMore': self.page.has_next(),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'items': data
        })