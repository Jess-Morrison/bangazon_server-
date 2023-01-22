from django.db import models
# from .product import Product 
# from .order_products import OrderProducts

class Order(models.Model):
  customer = models.ForeignKey("User", on_delete=models.CASCADE)
  # products = models.ForeignKey("Product", on_delete=models.CASCADE, unique=True)
  # order_products = models.ManyToManyField(OrderProducts)
  total_cost = models.FloatField()
  date_created = models.DateField()
  completed = models.BooleanField()
  quantity = models.IntegerField(default=0)
  
  @property
  def order_products(self):
        return self.__products

  @order_products.setter
  def order_products(self, value):
        self.__products = value

  @property
  def order_payment_types(self):
        return self.__payment_types

  @order_payment_types.setter
  def order_payment_types(self, value):
        self.__payment_types = value
