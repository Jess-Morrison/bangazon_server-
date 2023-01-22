from django.db import models
from .order import Order
from .payment_type import PaymentType 


class OrderProducts(models.Model):

    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete = models.CASCADE)
