# from turtle import title
from django.db import models 
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
import os


# Create your models here.


# Model Users 
class User(AbstractUser):
    
    GENDER_TYPE_CHOICES = ( 
        ('0', 'male'), 
        ('1', 'female'), 
		('2', 'other')
    )
    
    ACCOUNT_TYPE_CHOICES = ( 
        ('0', 'Administrator'), 
        ('1', 'Merchant'), 
		('2', 'Client')
    )

    def get_upload_path(instance, filename):
        return 'users/{0}/{1}'.format(instance.username, filename)
    
    email = models.EmailField(unique=True)
    
    gender = models.CharField(max_length=50, choices=GENDER_TYPE_CHOICES, default='2')

    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES, default='1')

    photo = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

