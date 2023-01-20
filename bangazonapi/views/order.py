from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User, Product, Order


class OrderView(ViewSet):
    """Level up user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single order

        Returns:
            Response -- JSON serialized order
        """
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all orders

        Returns:
            Response -- JSON serialized list of orders
        """
        orders = Order.objects.all() 
        serializer = OrderSerializer(orders, many = True)
        return Response(serializer.data)
      
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized order instance
        """
        customer = User.objects.get(id=request.data["customer"])

        order = Order.objects.create(
        total_cost=request.data["total_cost"],
        date_created=request.data["date_created"],
        completed=request.data["completed"],
        quantity=request.data["quantity"],
        customer=customer
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a product

        Returns:
            Response -- Empty body with 204 status code
        """

        order = Order.objects.get(pk=pk)
        order.total_cost = request.data["total_cost"]
        order.date_created = request.data["date_created"]
        order.completed = request.data["completed"]
        order.quantity = request.data["quantity"]
        

        customer = User.objects.get(pk=request.data["customer"])
        order.customer = customer
        order.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT) 
    
    def destroy(self, request, pk):
        order= Order.objects.get(pk=pk)
        order.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for products
    """
    class Meta:
        model = Order
        fields = ('id', 'total_cost', 'date_created', 'completed',  'customer', 'quantity') 
        depth = 1
