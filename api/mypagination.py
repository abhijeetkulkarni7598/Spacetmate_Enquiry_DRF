from rest_framework.pagination import PageNumberPagination

class MyLimit(PageNumberPagination):
    page_size = 10
