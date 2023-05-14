from rest_framework import serializers
from .models import CharacterCard


class CharacterCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterCard
        fields = [
            "id",
            "rating",
            "character",
            "type",
            "image",
        ]
