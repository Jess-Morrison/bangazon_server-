from django.db import models
# from .product import Product 
# from .order_products import OrderProducts

class Order(models.Model):
  customer = models.ForeignKey("User", on_delete=models.CASCADE)
  products = models.ManyToManyField("Product", through="OrderProducts", related_name="order")
  # order_products = models.ForeignKey("OrderProducts", on_delete=models.CASCADE)
  payment_types = models.ForeignKey("PaymentType", on_delete=models.CASCADE)
  total_cost = models.FloatField()
  date_created = models.DateField()
  completed = models.BooleanField()
  quantity = models.IntegerField(default=0)
  
  @property
  def order_products_prop(self):
        return self.__order_products_prop

  @order_products_prop.setter
  def order_products(self, value):
        self.__order_products_prop= value
        
  # @property
  # def order_products_prop(self):
  #       return self.__products

  # @order_products_prop.setter
  # def order_products(self, value):
  #       self.__products = value

  @property
  def order_payment_types(self):
        return self.__payment_types

  @order_payment_types.setter
  def order_payment_types(self, value):
        self.__payment_types = value
