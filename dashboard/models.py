from django.db import models

from django.utils import timezone
from account.models import *


# Create your models here.


class GiftCard(models.Model):
    
    title = models.CharField(max_length=255, unique=True, blank=False, null=False)
    slug = models.CharField(max_length=255, unique=True)
    
    code = models.CharField(max_length=15, default="", blank=False, null=False)
    amount = models.FloatField(default=0, blank=False, null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'CartKado ' + str(self.title) + ' : ' + str(self.amount) + ' €'


class Debit(models.Model):
    card = models.ForeignKey(GiftCard, on_delete=models.CASCADE)
    merchant = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    debit_amount = models.FloatField(default=0, blank=False, null=False)
    status = models.CharField(max_length=35, default="", blank=False, null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.merchant) + ' - ' + str(self.card) + ' - ' + str(self.debit_amount) + ' €'


