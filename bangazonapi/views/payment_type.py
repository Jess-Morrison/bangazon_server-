from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import PaymentType


class PaymentTypeView(ViewSet):
    """Level up payment type view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        payment_type = PaymentType.objects.get(pk=pk)
        serializer = PaymentTypeSerializer(payment_type)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all products

        Returns:
            Response -- JSON serialized list of products
        """
        payment_types = PaymentType.objects.all() 
        serializer = PaymentTypeSerializer(payment_types, many = True)
        return Response(serializer.data)

class PaymentTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = PaymentType
        fields = ('payment_name', 'account_number') 
        depth = 1
