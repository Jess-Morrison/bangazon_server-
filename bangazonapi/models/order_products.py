from django.db import models
from .order import Order
from .product import Product 


class OrderProducts(models.Model):
    customer = models.ForeignKey("User", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete = models.CASCADE)
    product = models.ForeignKey("Product", on_delete = models.CASCADE)
