from django.contrib import admin
from django.urls import path,include
from vendor.views import *
from vendor import views
from rest_framework import routers



router=routers.DefaultRouter()
# router.register(r'companies',ComapnyViewSet)
#
# router.register('singer',views.SingerViewSet,basename='singer')
# router.register('song',views.SongViewSet,basename='song')
router.register('vendor',views.VendorViewSet,basename='vendor')
router.register('employee',views.EmployeeViewSet,basename='employee')
urlpatterns = [
    path('',include(router.urls)),



]