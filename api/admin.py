from django.contrib import admin

# Register your models here.

from .models import *
# admin.site.register(Student)
# admin.site.register(Book)
# admin.site.register(Category)
# admin.site.register(Song)
# admin.site.register(Singer)
admin.site.site_header="Spacemate"
admin.site.site_title="Spacemate"
admin.site.index_title="Spacemate"
admin.site.register(Quotation)
# admin.site.register(User)
admin.site.register(Items)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(InteriorGallery)
admin.site.register(DesignGallery)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
 list_display=['id','contact_person_name','company_name']

# @admin.register(Inventorys)
# class InventorysAdmin(admin.ModelAdmin):
#  list_display=['id','sac','rate']
# admin.site.register(Shipping)