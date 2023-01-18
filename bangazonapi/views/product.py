from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User, Product


class ProductView(ViewSet):
    """Level up user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all products

        Returns:
            Response -- JSON serialized list of products
        """
        products = Product.objects.all() 
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)
      
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        seller = User.objects.get(id=request.data["seller"])

        product = Product.objects.create(
        price=request.data["price"],
        title=request.data["title"],
        description=request.data["description"],
        image_url=request.data["image_url"],
        quantity_available=request.data["quantity_available"],
        seller=seller
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a product

        Returns:
            Response -- Empty body with 204 status code
        """

        product = Product.objects.get(pk=pk)
        product.title = request.data["title"]
        product.price = request.data["price"]
        product.description = request.data["description"]
        product.image_url = request.data["image_url"]
        product.quantity_available = request.data["quantity_available"]

        seller = User.objects.get(pk=request.data["seller"])
        product.seller = seller
        product.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT) 
    
    def destroy(self, request, pk):
        product= Product.objects.get(pk=pk)
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Product
        fields = ('id', 'seller', 'price', 'title', 'description', 'image_url', 'quantity_available') 
        depth = 1
