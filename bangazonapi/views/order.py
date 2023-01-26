from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User, Product, Order, PaymentType, OrderProducts
from bangazonapi.views import product



class OrderView(ViewSet):
    """Level up user view"""

    def retrieve(self, request, pk, **kwargs):
        """Handle GET requests for single order

        Returns:
            Response -- JSON serialized order
        """
        order = Order.objects.get(pk=pk)
        product = Product.objects.get(pk=pk)
        order_products = OrderProducts.objects.filter(order=order, product=product)
        print(order_products)
        # if order.id == order_products:
        #   order = order.filter(order=order_products)
        
        data=[]
        
        serializer = OrderSerializer(order) 
        product_serializer = ProductSerializer(product)
        data.append(serializer)
        data.append(product_serializer)
        print(data)
        
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
      
    @action(methods=['post'], detail=True)
    def purchase(self, request, pk):
        """Post request to purchase a item"""

        product = Product.objects.get(pk=request.data["id"])
        # print(product)
        order = Order.objects.get(pk=pk)
        OrderProducts.objects.create(
            product=product,
            order=order
        )
        return Response({'message': 'Product added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def remove(self, request, pk):
        """Post request for a user to sign up for an event"""
        # 1. Use delete method and detail as true sincewe are using the primary key
        # Grabbing the user id and the event primary key
        #Do a filter where if the gamer and event in eventGamer matches the gamer and event that is listed in the object
        # if they match, then you delete 

        product = Product.objects.get(pk=request.data["id"])
        order = Order.objects.get(pk=pk)
        orderProducts= OrderProducts.objects.filter(
            product = product,
            order = order
        )
        orderProducts.delete()
       
          
        return Response({'message': 'Product removed'}, status=status.HTTP_204_NO_CONTENT)  
      
    @action(methods=['post'], detail=True)
    def payment_of_choice(self, request, pk):
        """Post request to choose payment type"""

        payment_type = PaymentType.objects.get(pk=request.data["id"])
        # print(product)
        order = Order.objects.get(pk=pk)
        OrderProducts.objects.create(
            payment_type=payment_type,
            order=order
        )
        return Response({'message': 'Payment type added'}, status=status.HTTP_201_CREATED)
      
    @action(methods=['delete'], detail=True)
    def remove(self, request, pk):
        """Post request for a user to sign up for an event"""
        # 1. Use delete method and detail as true sincewe are using the primary key
        # Grabbing the user id and the event primary key
        #Do a filter where if the gamer and event in eventGamer matches the gamer and event that is listed in the object
        # if they match, then you delete 

        payment_type = PaymentType.objects.get(pk=request.data["id"])
        order = Order.objects.get(pk=pk)
        orderPaymentType= OrderProducts.objects.filter(
            payment_type = payment_type,
            order = order
        )
        orderPaymentType.delete()
       
          
        return Response({'message': 'Product removed'}, status=status.HTTP_204_NO_CONTENT)    
    
class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for products
    """
    class Meta:
        model = Order
        fields = ('id', 'total_cost', 'date_created', 'completed',  'customer', 'quantity', 'order_products') 
        depth = 1
        


class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for products
    """
    class Meta:
        model = Product
        fields = ('id', 'seller', 'price', 'title', 'description', 'image_url', 'quantity_available') 
        depth = 1
