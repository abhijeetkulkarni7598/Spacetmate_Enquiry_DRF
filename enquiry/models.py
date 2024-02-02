from django.db import models
from app.models import UserAccount
from django.utils import timezone

class Enquire(models.Model):

    STATUS_CHOICES = (
        ('Enquiry', 'Enquiry'),
        ('Prospect', 'Prospect'),
        ('Client', 'Client'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Enquiry")

    name = models.CharField(max_length=255)
    mobile = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=255, blank=True, null=True)
    requirement = models.TextField(blank=True, null=True)
    floor_plain = models.FileField(upload_to='floor_plans/', blank=True, null=True)
    created_by=models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True, related_name='created_by')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True,related_name="user")

    def __str__(self):
        return self.name
    

class Design(models.Model):
    STATUS_CHOICES = (
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    )

    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='designs/', blank=True, null=True)
    approval = models.CharField(max_length=20, choices=STATUS_CHOICES)
    enquiry = models.ForeignKey(Enquire, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

from django import forms
from django.contrib import admin
from .models import Enquire, Design
class EnquireAdminForm(forms.ModelForm):
    class Meta:
        model = Enquire
        exclude = ()

    user = forms.ModelChoiceField(
        queryset=UserAccount.objects.filter(is_customer=True),
        label="User",
    )



from django import forms
from django.contrib import admin
from .models import Enquire, Design
class EnquireAdmin(admin.ModelAdmin):
    form = EnquireAdminForm
    list_display = ['name', 'mobile', 'email', 'address', 'requirement', 'user']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = UserAccount.objects.filter(is_customer=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)