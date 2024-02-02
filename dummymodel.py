from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,Group,Permission,BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        if  not email:
            raise ValueError('User Must have an email')

        email=self.normalize_email(email)
        user=self.model(email=email,name=name)
        # user.is_superuser = True
        user.set_password(password)
        user.save()

        return user

class UserAccount(AbstractBaseUser,PermissionsMixin):
    email = models.CharField(max_length=255, unique=True,blank=True)
    name = models.CharField(max_length=255,blank=True)
    is_active = models.BooleanField(default=True,blank=True)
    is_staff = models.BooleanField(default=True,blank=True)
    is_admin = models.BooleanField(default=False,blank=True)
    view = models.BooleanField(default=False,blank=True)
    create = models.BooleanField(default=False,blank=True)
    objects=UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name']

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='user_accounts'  # Change the related_name
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_accounts'  # Change the related_name
    )

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name
    
    def __str__(self):
        return self.email
    



class Student(models.Model):
    name=models.CharField(max_length=50)
    roll=models.IntegerField()
    city=models.CharField(max_length=50)



class Question(models.Model):
    title=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    created_by=models.CharField(max_length=50)


class Choices(models.Model):
    question=models.CharField(max_length=50)
    text=models.CharField(max_length=50)