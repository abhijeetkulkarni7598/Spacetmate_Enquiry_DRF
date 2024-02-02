from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from vendor.models import *
from vendor.serializers import *
from .mypagination import MyLimit
# Create your views here.
class VendorViewSet(viewsets.ModelViewSet):
    
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    pagination_class = MyLimit
    filter_backends = [SearchFilter]
    search_fields = ["name"]
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     user_client_id = self.request.query_params.get("name")
    #     user_client_id2 = self.request.query_params.get("number")

    #     if user_client_id:
    #         queryset = queryset.filter(name=user_client_id)
    #     if user_client_id2:
    #         queryset = queryset.filter(number=user_client_id2)

    #     return queryset


class EmployeeViewSet(viewsets.ModelViewSet):
    
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # search_fields=['item_name','item_category']
    pagination_class = MyLimit
    filter_backends = [SearchFilter]
    search_fields = ["name"]