from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User


class UserView(ViewSet):
    """Bangazon User view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        bangazon_user = User.objects.get(pk=pk)
        serializer = UserSerializer(bangazon_user)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all users

        Returns:
            Response -- JSON serialized list of users
        """
        bangazon_users = User.objects.all()  
        serializer = UserSerializer(bangazon_users, many = True)
        return Response(serializer.data)
      
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized user instance
        """
        bangazon_user = User.objects.get(uid=request.data["user_id"])

        bangazon_user = User.objects.create(
        first_name = request.data["first_name"],
        last_name = request.data["last_name"],
        uid = request.data["uid"],
        created_on = request.data["created_on"],
        image_url = request.data["image_url"]
        
        )
        serializer = UserSerializer(bangazon_user)
        return Response(serializer.data)  

    def update(self, request, pk):
        bangazon_user = User.objects.get(pk=pk)
        bangazon_user.first_name = request.data["first_name"]
        bangazon_user.last_name = request.data["last_name"]
        bangazon_user.uid = request.data["uid"]
        bangazon_user.created_on = request.data["created_on"]
        bangazon_user.image_url = request.data["image_url"]
        bangazon_user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # @action(methods=['put'], detail=True)
    # def change_is_staff(self, request, pk):
    #     rare_user = RareUser.objects.get(pk=pk)

    #     rare_user.is_staff = not rare_user.is_staff
    #     rare_user.save()
    #     serializer = UserSerializer(rare_user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(methods=['put'], detail=True)
    # def change_is_active(self, request, pk):
    #     rare_user = RareUser.objects.get(pk=pk)

    #     rare_user.active = not rare_user.active
    #     rare_user.save()
    #     serializer = UserSerializer(rare_user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for rare users"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'uid', 'created_on', 'image_url')
