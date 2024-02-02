from django.contrib import admin
from django.urls import path,include
from api.views import *
from api import views
from rest_framework import routers

router=routers.DefaultRouter()
# router.register(r'companies',ComapnyViewSet)
#
# router.register('singer',views.SingerViewSet,basename='singer')
# router.register('song',views.SongViewSet,basename='song')
router.register('quotation',views.QuotationViewSet,basename='quotation')
router.register('quotation2',views.QuotationViewSet2,basename='quotation')

router.register('item',views.ItemViewSet,basename='item')
router.register('items',views.ItemsViewSet,basename='items')

router.register('client',views.ClientViewSet,basename='client')
# router.register('shipping',views.ShippingViewSet,basename='shipping')

router.register('inventory',views.InventoysViewSet,basename='inventory')
router.register('category',views.CategoryViewSet,basename='category')
router.register('status',views.StatusViewSet,basename='status')
router.register('image',views.ImageViewSet,basename='image')
router.register('designimage',views.DesignGalleryViewSet,basename='designimage')

urlpatterns = [
    path('',include(router.urls)),
    path('status-count/', QuotationNumberCountView.as_view(), name='quotation_number_count'),
    path('item_category-count/', ItemsViewStatistic.as_view(), name='items_number_count'),
    path('user-count/', UserViewStatistic.as_view(), name='user_number_count'),
    path('revinue/', RevinueViewSet.as_view(), name='revinue-api'),
    path('revinuer01/', RevinueR01ViewSet.as_view(), name='revinuer01-api'),
    path('deal-won/', DealWonRevinueViewSet.as_view(), name='deal_won-api'),


]