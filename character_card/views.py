import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import generics

from beta_user.models import (
    BetaUser,
    UserCharacterCard,
)

from .models import CharacterCard
from .serializers import CharacterCardSerializer


class CharacterCardList(generics.ListCreateAPIView):
    queryset = CharacterCard.objects.all()
    serializer_class = CharacterCardSerializer


class CharacterCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CharacterCard.objects.all()
    serializer_class = CharacterCardSerializer


@csrf_exempt
@require_http_methods(["POST"])
def get_all_character_cards(request):
    character_cards = CharacterCard.objects.all().order_by(
        "character__serie__name_en",
    )
    character_card_list = []

    character_card_list = []
    user_list = list(BetaUser.objects.exclude(username="admin"))
    for character_card in character_cards:
        user_per_list = []
        for user in user_list:
            counter = UserCharacterCard.objects.filter(
                user = user,
                character_card = character_card,
            ).count()
            if counter > 0:
                user_per_list.append({
                    "name": user.username,
                    "count": counter,
                })
        character_card_list.append({
            "card_id": character_card.id,
            "rating": character_card.rating,
            "name": character_card.character.name,
            "serie": character_card.character.serie.name_en,
            "image_url": character_card.image.url,
            "type": character_card.type,
            "user_info": user_per_list,
        })

    return JsonResponse({
        "character_cards": character_card_list,
    })
