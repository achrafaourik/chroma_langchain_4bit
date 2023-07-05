"""
Serializers for Item APIs
"""
from rest_framework import serializers
from core.models import Coin


class UpdateCoinsSerializer(serializers.Serializer):
    number_of_coins = serializers.IntegerField()
    operation = serializers.ChoiceField(choices=["add", "remove"])


class CoinSerializer(serializers.ModelSerializer):
    """Serializer for Items."""

    class Meta:
        model = Coin
        # fields = ['id', 'title', 'price', 'link']
        fields = ['id', 'num_coins', 'level']
        read_only_fields = ['id']


class CoinDetailSerializer(CoinSerializer):
    """Serializer for Item detail view."""

    class Meta(CoinSerializer.Meta):
        fields = CoinSerializer.Meta.fields + ['transaction_id']
