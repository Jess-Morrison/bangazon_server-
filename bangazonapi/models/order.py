from django.db import models
class Order(models.Model):
  customer = models.ForeignKey("User", on_delete=models.CASCADE)
  total_cost = models.FloatField()
  date_created = models.DateField()
  completed = models.BooleanField()
  quantity = models.IntegerField(default=0)
  
