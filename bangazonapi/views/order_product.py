from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import  Order,OrderProducts

class OrderProductsView(ViewSet):
    """Level up user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single order

        Returns:
            Response -- JSON serialized order
        """
        order_products = OrderProducts.objects.get(pk=pk)
        # orders = Order.objects.get(id=request.data["order"])
        orders = request.query_params.get('order', None)
        if order_products.id == orders:
          order_products = order_products.filter(orders=order_products)
        
        serializer = OrderProductSerializer(order_products)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all orders

        Returns:
            Response -- JSON serialized list of orders
        """
        order_products = OrderProducts.objects.all() 
        serializer = OrderProductSerializer(order_products, many = True)
        return Response(serializer.data)

class OrderProductSerializer(serializers.ModelSerializer):
    """JSON serializer for products
    """
    class Meta:
        model = OrderProducts
        fields = ('id', 'order', 'product') 
        depth = 1