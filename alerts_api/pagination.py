from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 50


