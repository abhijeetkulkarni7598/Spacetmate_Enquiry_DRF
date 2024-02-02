# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import *

router = DefaultRouter()
router.register(r'enquires', EnquireViewSet, basename='enquire')
router.register(r'designs', DesignViewSet, basename='design')
router.register('designx',DesignaViewSet,basename='designx')

urlpatterns = [
    path('', include(router.urls)),
]