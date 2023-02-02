from tkinter import TRUE
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
        #You will need to filter here in order to get the correct items to render to the DOM
        #First, get values by keys 
        #Query parameters are a set of key-value pairs that are appended to the end of a URL and used to pass additional information to the server. In Django, request.query_params is a dictionary-like object that contains the query parameters for a given request. 
        
        product = request.query_params.get('product')
        order = request.query_params.get('order')
        customer = request.query_params.get('customer')
        completed = request.query_params.get(False)
        
        order_products = OrderProducts.objects.all() 
        #Now filter out the data through the use of conditionals. I.e if this, filter by this,etc
        
        if completed is not TRUE:
            order_products = order_products.filter(completed=completed)
        if product is not None:
            order_products = order_products.filter(product=product)
        if order is not None:
            order_products = order_products.filter(order=order)
        if customer is not None:
            order_products = order_products.filter(customer=customer)
            
        serializer = OrderProductSerializer(order_products, many = True)
        return Response(serializer.data)
        
        # order = request.query_params.get('order_id', None)
        # if order is not None:
        #   order_products = order_products.filter(order=order)
        # serializer = OrderProductSerializer(order_products, many = True)
        # return Response(serializer.data)
        
    def update(self, request, pk):
      """Update a Order Product"""
      order_product = OrderProducts.objects.get(pk=pk)
      order_product.product = Product.objects.get(pk=request.data["product"])
      order_product.order = Order.objects.get(pk=request.data['order'])
      order_product.save()
      return Response({'success': True}, status=status.HTTP_202_ACCEPTED)
  
    def destroy(self, request, pk):
      """Delete a Order product"""
      order_product = OrderProducts.objects.get(pk=pk)
      order_product.delete()
      return Response(None, status=status.HTTP_204_NO_CONTENT)    
        

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
