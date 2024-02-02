from django.db import models

# Create your models here.
class Vendor(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    number=models.IntegerField(null=True,blank=True)
    email=models.CharField(max_length=100,null=True,blank=True)
    adhar_pan=models.CharField(max_length=100,null=True,blank=True)

    bank_name=models.CharField(max_length=100,null=True,blank=True)
    account_number=models.CharField(max_length=100,null=True,blank=True)
    ifsc=models.CharField(max_length=100,null=True,blank=True)
    
    upi_detials=models.CharField(max_length=100,null=True,blank=True)
    
    local_address=models.CharField(max_length=100,null=True,blank=True)
    permanent_address=models.CharField(max_length=100,null=True,blank=True)
    field_experience=models.CharField(max_length=100,null=True,blank=True)
    service_provided=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name
    
    
class Employee(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    number=models.IntegerField(null=True,blank=True)
    email=models.CharField(max_length=100,null=True,blank=True)
    adhar_pan=models.CharField(max_length=100,null=True,blank=True)
    bank_name=models.CharField(max_length=100,null=True,blank=True)
    account_number=models.CharField(max_length=100,null=True,blank=True)
    ifsc=models.CharField(max_length=100,null=True,blank=True)
    upi_detials=models.CharField(max_length=100,null=True,blank=True)
    local_address=models.CharField(max_length=100,null=True,blank=True)
    permanent_address=models.CharField(max_length=100,null=True,blank=True)
    field_experience=models.CharField(max_length=100,null=True,blank=True)
    service_provided=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name