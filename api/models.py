from django.db import models
from enquiry.models import Enquire
# from django.contrib.auth.models import *
# Create your models here.

#Creating company model




# class Singer (models.Model):
#     name=models.CharField(max_length=100)
#     gender=models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Song(models.Model):
#     title=models.CharField(max_length=100)
#     singer=models.ForeignKey(Singer,on_delete=models.CASCADE,related_name='sungby')
#     duration=models.IntegerField()

#     def __str__(self):
#         return self.title
# class UserAccount(AbstractBaseUser):
#     username = models.EmailField(max_length=255, unique=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     def __str__(self):
#         return self.username
STATE_CHOICE = (
    ("AS PER DESIGN", "AS PER DESIGN"),
    ("LENGTH HEIGHT", "LENGTH HEIGHT"),

)
UNIT = (
    ("SQR METER", "SQR METER"),
    ("MILI METER", "MILI METER"),
    ("INCH", "INCH"),
    ("SQR FOOT", "SQR FOOT"),
    ("RUNNING FOOT", "RUNNING FOOT"),
    ("NUMBERS", "NUMBERS"),
    ("APPROXIMATE","APPROXIMATE"),
    ("LUMPSUM","LUMPSUM"),


)

IMAGE_CHOICE = (
    ("COMMERCIAL", "COMMERCIAL"),
    ("HOME INTERIOR", "HOME INTERIOR"),
    ("RETAIL SHOP", "RETAIL SHOP"),


)
IMAGE_CHOICE2 = (
    ("2D", "2D"),
    ("3D", "3D"),


)

class Client(models.Model):
    contact_person_name=models.CharField(max_length=100,blank=True,null=True)
    # the person who made it
    user_client_id=models.IntegerField(blank=True,null=True)
    user_client_name=models.CharField(max_length=100,blank=True,null=True)

    allocate_name=models.CharField(max_length=100,blank=True,null=True)
    company_name=models.CharField(max_length=100,blank=True,null=True)
    email=models.CharField(max_length=100,blank=True,null=True)
    phone=models.CharField(max_length=100,blank=True,null=True)
    site_address=models.CharField(max_length=100,blank=True,null=True)
    
from datetime import datetime
class Quotation(models.Model):
    enquiry = models.ForeignKey(Enquire, on_delete=models.CASCADE, null=True, blank=True)
    quotation_number=models.CharField(max_length=100,blank=True,null=True,default="20")

    user_client=models.CharField(max_length=100,blank=True,null=True)
    user_client_id=models.IntegerField(blank=True,null=True)
    client_id=models.CharField(max_length=100,blank=True,null=True)
    client_name=models.CharField(max_length=100,blank=True,null=True)
    client_address=models.CharField(max_length=100,blank=True,null=True)
    client_contact=models.CharField(max_length=100,blank=True,null=True)
    special_note=models.CharField(max_length=500,blank=True,null=True)
    remark=models.CharField(max_length=500,blank=True,null=True)
    discount=models.IntegerField(null=True,blank=True)
    total_with_discount=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    date=models.CharField(max_length=100,blank=True,null=True,default=datetime.now().strftime("%d/%m/%y"))
    revision_no=models.CharField(max_length=100,blank=True,null=True)
    status=models.IntegerField(blank=True,null=True)



    def __str__(self):
        return self.quotation_number
    @property
    def item(self):
        return self.choice_set.all()


# inside quotation

class Item(models.Model):
    item_name=models.CharField(max_length=100,null=True,blank=True)
    item_category=models.CharField(max_length=100,null=True,blank=True)
    size=models.CharField(max_length=100,blank=True,null=True)
    unit=models.CharField(max_length=100,blank=True,null=True)

    height=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    length=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    sqft=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    width=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    depth=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)

    item_id=models.IntegerField(null=True,blank=True)
    costing=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    total=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)


    numbers=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    running_foot=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    quantity=models.DecimalField(null=True,blank=True,default=1,max_digits=20,decimal_places=2)
    specifications=models.CharField(max_length=500,blank=True,null=True)

    quotation=models.ForeignKey(Quotation,on_delete=models.CASCADE,related_name='item')


    def __str__(self):
        return self.item_name

    @property
    def votes(self):
        return self.answer_set.count()

# independent
class Items(models.Model):
    item_name=models.CharField(max_length=100,null=True,blank=True)
    item_category=models.CharField(max_length=100,null=True,blank=True)
    unit=models.CharField(max_length=100,blank=True,null=True,choices=UNIT)
    height=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)

    width=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    depth=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)

    length=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    sqft=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    numbers=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    running_foot=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    specifications=models.CharField(max_length=500,blank=True,null=True)
    costing=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    quantity=models.DecimalField(null=True,blank=True,default=1,max_digits=20,decimal_places=2)

    def __str__(self):
        return self.item_name

# independent
class Category(models.Model):
    category=models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.category


#independent
class Status(models.Model):
    status=models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.status


class Inventorys(models.Model):
    product_name=models.CharField(max_length=100,null=True)
    sac=models.IntegerField(null=True)
    rate=models.IntegerField(null=True)
    total_quantity=models.IntegerField(null=True,blank=True)
    unit=models.CharField(max_length=100,null=True)


class InteriorGallery(models.Model):
    image = models.ImageField(upload_to='img/', null=True)
    imageName=models.CharField(max_length=100,null=True)
    tag=models.CharField(max_length=100,null=True,choices=IMAGE_CHOICE)

    def __str__(self):
        return self.imageName
class DesignGallery(models.Model):
    image = models.ImageField(upload_to='img/', null=True)
    imageName=models.CharField(max_length=100,null=True)

    tag=models.CharField(max_length=100,null=True,choices=IMAGE_CHOICE2)

    def __str__(self):
        return self.imageName









# unit pageination client id