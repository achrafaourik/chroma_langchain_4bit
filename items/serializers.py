"""
Serializers for Item APIs
"""
from rest_framework import serializers

from core.models import Item


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Items."""

    class Meta:
        model = Item
        # fields = ['id', 'title', 'price', 'link']
        fields = ['id', 'title']
        read_only_fields = ['id']


class ItemDetailSerializer(ItemSerializer):
    """Serializer for Item detail view."""

    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + ['description']
