from django.db import models

class PaymentType(models.Model):
  
  payment_name = models.CharField(max_length=50)
  account_number = models.IntegerField(default=0)
  
