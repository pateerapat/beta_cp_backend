from rest_framework import serializers
from .models import CardPack


class CardPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardPack
        fields = [
            "id",
            "title",
            "include_ratings",
            "include_character_cards",
            "include_series",
            "description",
            "price",
            "image",
        ]
