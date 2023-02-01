from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import  Order,OrderProducts
from rest_framework import generics

from bangazonapi.models.product import Product

class OrderProductsView(ViewSet):
    """Level up user view"""

    def retrieve(self, request, order):
        """Handle GET requests for single order

        Returns:
            Response -- JSON serialized order
        """
        order_products = OrderProducts.objects.filter(order)
        # orders = Order.objects.filter(id=order_products.order.id)
        # print(order_products)
        # # orders = Order.objects.get(pk-pk)
        # # orders = request.query_params.get('order', None)
        # if orders == order_products:
        #   order_products = order_products.filter(orders=orders)
        
        
        serializer = OrderProductSerializer(order_products)
        return Response(serializer.data)

    def list(self,request):
        """Handle GET requests to get all orders
        Put in a query string

        Returns:
            Response -- JSON serialized list of orders
        """
        order_products = OrderProducts.objects.all() 
        order = request.query_params.get('order_id', None)
        if order is not None:
          order_products = order_products.filter(order=order)
        serializer = OrderProductSerializer(order_products, many = True)
        return Response(serializer.data)

class OrderProductSerializer(serializers.ModelSerializer):
    """JSON serializer for products
    """
    class Meta:
        model = OrderProducts
        fields = ('id', 'order', 'product', 'customer') 
        depth = 1

# class OrderJointView(generics.ListCreateAPIView):
#   serializer_class = OrderProductSerializer
#   def get_queryset(self):
#     product_id = self.kwargs['products_id']
#     return Order.objects.filter(products_id=product_id)
  
# class ProductJointView(generics.ListCreateAPIView):
#     serializer_class = OrderProductSerializer
#     def get_queryset(self):
#       product_id = self.kwargs['product_id']
#       return Order.objects.filter(product__id=product_id)
