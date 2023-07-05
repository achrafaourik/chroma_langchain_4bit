"""
Views for the Coin APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Coin
from coins import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes




class CoinViewSet(viewsets.ModelViewSet):
    """View for manage Item APIs."""
    serializer_class = serializers.CoinDetailSerializer
    queryset = Coin.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve Items for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.CoinSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Item."""
        serializer.save(user=self.request.user)


    @extend_schema(request=serializers.UpdateCoinsSerializer, responses=OpenApiTypes.OBJECT)
    @action(detail=False, methods=['post'], url_path='update-coins')
    def update_coins(self, request):
        coin = self.request.user.coin
        number_of_coins_to_update = request.data.get('number_of_coins', 0)
        operation = request.data.get('operation')

        if operation == 'add':
            coin.num_coins += int(number_of_coins_to_update)
        elif operation == 'remove':
            if coin.num_coins < int(number_of_coins_to_update):
                raise ValidationError('Insufficient coins.')
            coin.num_coins -= int(number_of_coins_to_update)
        else:
            raise ValidationError('Invalid operation.')

        coin.save()
        return Response({'status': 'number of coins updated'}, status=status.HTTP_200_OK)
