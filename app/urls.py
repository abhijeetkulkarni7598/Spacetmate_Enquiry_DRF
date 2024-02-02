# from django.contrib import admin
from django.urls import path,include
from app.views import *
# from api import views
from rest_framework import routers
router=routers.DefaultRouter()

from app import views
from rest_framework import routers



router=routers.DefaultRouter()
# router.register(r'companies',ComapnyViewSet)
#
# router.register('singer',views.SingerViewSet,basename='singer')
# router.register('song',views.SongViewSet,basename='song')
router.register('profile',views.ProfileViewSet,basename='profile')
urlpatterns = [
    path('',include(router.urls)),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('auth/users/reset_password/', CustomPasswordResetView.as_view({'post': 'list'}), name='password_reset'),
    path('userinfo', views.userinfo, name="userinfo"),
    path('customer-user/', views.get_all_users, name="user"),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('customer/', UserRegistrationCustomerView.as_view(), name='customer-registration'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    # path('login/', CustomLoginView.as_view(), name='custom_login'),
    #  path('login/', custom_login_view, name='custom_login'),
    # path('login/', UserLoginView.as_view(), name='user-login'),


]
