import json
import numpy

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import generics

from beta_user.models import (
    BetaUser,
    UserCardPack,
    UserCharacterCard,
)
from character_card.models import (
    CharacterCard,
    CharacterRating,
)
from notification.models import Notification

from .models import CardPack
from .serializers import CardPackSerializer


class CardPackList(generics.ListCreateAPIView):
    queryset = CardPack.objects.all()
    serializer_class = CardPackSerializer


class CardPackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CardPack.objects.all()
    serializer_class = CardPackSerializer


@csrf_exempt
@require_http_methods(["POST"])
def get_shop_card_packs(request):
    object_pack_by_series = CardPack.objects.filter(is_by_series=True, is_active=True)
    object_pack_by_event = CardPack.objects.filter(is_by_event=True, is_active=True)
    object_pack_by_custom = CardPack.objects.filter(is_by_event=False, is_by_series=False, is_active=True)

    pack_by_series = []
    pack_by_event = []
    pack_by_custom = []
    counter = 0
    for tier in [object_pack_by_series, object_pack_by_event, object_pack_by_custom]:
        for pack in tier:
            rating_from = None
            rating_to = None
            for index, rating in enumerate(pack.include_ratings):
                if index == 0:
                    rating_from = rating
                if index == len(pack.include_ratings) - 1:
                    rating_to = rating

            series = []
            for serie in pack.include_series.all():
                series.append(serie.name_en)

            data = {
                "pack_id": pack.id,
                "rating_from": rating_from,
                "rating_to": rating_to,
                "name": pack.title,
                "series": series,
                "price": pack.price,
                "image_url": pack.image.url,
                "is_new": pack.is_new,
            }
            if counter == 0:
                pack_by_series.append(data)
            elif counter == 1:
                pack_by_event.append(data)
            elif counter == 2:
                pack_by_custom.append(data)
        counter += 1

    return JsonResponse({
        "pack_by_series": pack_by_series,
        "pack_by_event": pack_by_event,
        "pack_by_custom": pack_by_custom,
    })


@csrf_exempt
@require_http_methods(["POST"])
def purchase_pack(request):
    json_data = json.loads(request.body)
    user_id = json_data.get("user")
    pack_id = json_data.get("packId")
    current_user = BetaUser.objects.get(pk=user_id)
    assosiated_card_pack = CardPack.objects.get(pk=pack_id)

    if current_user.moonstone >= assosiated_card_pack.price:
        current_user.moonstone -= assosiated_card_pack.price
        current_user.save()
        UserCardPack.objects.create(
            user_id        = user_id,
            card_pack_id   = pack_id,
        )
        return JsonResponse({
            "success": True,
        })
    else:
        return JsonResponse({
            "success": False,
        })


@csrf_exempt
@require_http_methods(["POST"])
def open_pack(request):
    json_data = json.loads(request.body)
    user_id = json_data.get("user")
    pack_id = json_data.get("packId")
    user_pack_id = json_data.get("userPackId")

    assosiated_card_pack = CardPack.objects.get(pk=pack_id)
    all_characters_in_series = CharacterCard.objects.filter(
        character__serie__in = list(assosiated_card_pack.include_series.all()),
    )
    all_characters_in_series = all_characters_in_series.filter(
        rating__in = list(assosiated_card_pack.include_ratings),
    )
    all_characters = assosiated_card_pack.include_character_cards.filter(
        rating__in = list(assosiated_card_pack.include_ratings),
    )
    final_characters_list = all_characters_in_series | all_characters
    final_characters_list = final_characters_list.distinct()

    ratings_rule = assosiated_card_pack.ratings_rule.replace("[", "")
    ratings_rule = ratings_rule.replace("]", "")
    ratings_rule = ratings_rule.split(",")

    ratings_rule = list(map(float, ratings_rule))

    final_rating = numpy.random.choice(numpy.arange(0, len(assosiated_card_pack.include_ratings)), p=ratings_rule)
    final_rating = assosiated_card_pack.include_ratings[final_rating]

    correct_rating_characters = final_characters_list.filter(
        rating = final_rating,
    )

    random_card_index = numpy.random.randint(0, correct_rating_characters.count(), 1)
    random_card_index = int(random_card_index[0])
    selected_character_card = correct_rating_characters[random_card_index]
    created_character_card = UserCharacterCard.objects.create(
        user_id             = user_id,
        character_card_id   = selected_character_card.id,
    )
    character_card_info = {
        "id": created_character_card.id,
        "card_id": created_character_card.character_card.id,
        "rating": created_character_card.character_card.rating,
        "name": created_character_card.character_card.character.name,
        "serie": created_character_card.character_card.character.serie.name_en,
        "image_url": created_character_card.character_card.image.url,
        "type": created_character_card.character_card.type,
    }
    if selected_character_card.rating == CharacterRating.RARE:
        Notification.objects.create(
            user_id             = user_id,
            character_card_id   = selected_character_card.id,
            card_pack_id        = assosiated_card_pack.id,
        )
    UserCardPack.objects.filter(pk=user_pack_id).delete()
    return JsonResponse({
        "success": True,
        "character_card": character_card_info,
    })
