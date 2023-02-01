from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User, Product, Order, PaymentType, OrderProducts
from rest_framework import generics
from rest_framework.decorators import action



class OrderView(ViewSet):
    """Level up user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single order

        Returns:
            Response -- JSON serialized order
        """
        order = Order.objects.get(pk=pk)
        # order_products = OrderProducts.objects.filter("order")
        # if order == order_products:
        #   order = order.filter(order_products=order_products)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all the orders

        Returns:
            Response -- JSON serialized list of orders
        """
        # orders = Order.objects.all() 
        # serializer = OrderSerializer(orders, many = True)
        # return Response(serializer.data)
        orders = Order.objects.all()
 
        customer = request.query_params.get('user', None)
        if customer is not None:
            orders = orders.filter(customer_id=customer)
            
        completed = request.query_params.get('closed', None)
        if completed is not None:
            if completed == "true":
            
                completed = True
            else:
                completed= False
            
            orders = orders.filter(is_closed=completed)
        for order in orders:
            products_on_order = OrderProducts.objects.filter(order=order.id)
            order_products_prop = []
            
            for product_order_obj in products_on_order:
                
                product_dict={}
                try:
                    products_on_order = Product.objects.get(id=product_order_obj.product_id)
                    product_dict['id']=products_on_order.id
                    product_dict['title']=products_on_order.title
                    product_dict['image_url']=products_on_order.image_url
                except:
                    pass
                
      
                seller_info = User.objects.get(id=products_on_order.seller.id)
                product_dict['first_name']=seller_info.first_name
                product_dict['last_name']=seller_info.last_name
            
                order_products_prop.append(product_dict)
                        
            order.associated_products = order_products_prop
            
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
      
    def create(self, request, pk):
        """Handle POST operations

        Returns
            Response -- JSON serialized order instance
        """
        customer = User.objects.get(pk=request.data["customer_id"])
        payment_type = PaymentType.objects.get(pk=request.data['payment_types_id'])
      

        order = Order.objects.create(
        total_cost=request.data["total_cost"],
        date_created=request.data["date_created"],
        completed= True,
        quantity=request.data["quantity"],
        customer=customer,
        payment_type = payment_type
        )
        order_products_prop = request.data['order_products_prop']
        products = [Product.objects.get(pk=product_id) for product_id in order_products_prop]
        
        for product in products:
            order_products = OrderProducts(product=product, order=order)
            order_products.save()
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
        order.payment_types = request.data["payment_types"]
        

        # customer = User.objects.get(pk=request.data["customer"])
        products = Product.objects.get(pk=request.data['products'])
        # order.customer = customer
        order.products = products
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
        fields = ('id', 'total_cost', 'date_created', 'completed',  'customer', 'quantity', 'payment_types') 
        depth = 2
        
class OrderProductSerializer(serializers.ModelSerializer):
    """JSON serializer for products
    """
    class Meta:
        model = OrderProducts
        fields = ('id', 'order', 'product', 'customer') 
        depth = 2

class OrderJointView(generics.ListCreateAPIView):
  serializer_class = OrderProductSerializer
  def get_queryset(self):
    order_id = self.kwargs['order_id']
    return OrderProducts.objects.filter(order__id=order_id)
