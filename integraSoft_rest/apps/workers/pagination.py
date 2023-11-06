from rest_framework.pagination import PageNumberPagination

class CustomPaginationPeopleSoft(PageNumberPagination):
    page_size = 10  # Número de elementos por página
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Número máximo de elementos por página

class CustomPaginationHcm(PageNumberPagination):
    page_size = 10  # Número de elementos por página
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Número máximo de elementos por página