from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Enquire)
admin.site.register(Design)


admin.site.register(Enquire, EnquireAdmin)