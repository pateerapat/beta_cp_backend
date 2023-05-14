import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from beta_user.models import (
    BetaUser,
    UserCharacterCard,
    UserCardPack,
)

from character_card.models import CharacterRating


@csrf_exempt
@require_http_methods(["POST"])
def get_user_character_cards(request):
    json_data = json.loads(request.body)
    user_id = json_data.get("user")
    user_character_cards = UserCharacterCard.objects.filter(
        user = user_id,
    ).order_by(
        "-created",
    )

    character_card_list = []
    for character_card in user_character_cards:
        character_card_list.append({
            "id": character_card.id,
            "card_id": character_card.character_card.id,
            "rating": character_card.character_card.rating,
            "name": character_card.character_card.character.name,
            "serie": character_card.character_card.character.serie.name_en,
            "image_url": character_card.character_card.image.url,
            "type": character_card.character_card.type,
        })

    return JsonResponse({
        "character_cards": character_card_list,
    })


@csrf_exempt
@require_http_methods(["POST"])
def get_user_card_packs(request):
    json_data = json.loads(request.body)
    user_id = json_data.get("user")
    user_card_packs = UserCardPack.objects.filter(
        user = user_id,
    ).order_by(
        "-created",
    )

    card_pack_list = []
    for card_pack in user_card_packs:
        pack = card_pack.card_pack
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
            "id": card_pack.id,
            "pack_id": pack.id,
            "rating_from": rating_from,
            "rating_to": rating_to,
            "name": pack.title,
            "series": series,
            "price": pack.price,
            "image_url": pack.image.url,
            "is_new": pack.is_new,
        }
        card_pack_list.append(data)

    return JsonResponse({
        "card_packs": card_pack_list,
    })


@csrf_exempt
@require_http_methods(["POST"])
def sell_user_card(request):
    json_data = json.loads(request.body)
    user_card_id = json_data.get("userCardId")
    user_card_packs = UserCharacterCard.objects.get(
        id = user_card_id,
    )

    if user_card_packs.character_card.rating == CharacterRating.COMMON:
        user_card_packs.user.moonstone += 1
        user_card_packs.user.save()
    elif user_card_packs.character_card.rating == CharacterRating.UNCOMMON:
        user_card_packs.user.moonstone += 5
        user_card_packs.user.save()
    elif user_card_packs.character_card.rating == CharacterRating.RARE:
        user_card_packs.user.moonstone += 20
        user_card_packs.user.save()
    elif user_card_packs.character_card.rating == CharacterRating.EPIC:
        user_card_packs.user.moonstone += 100
        user_card_packs.user.save()
    elif user_card_packs.character_card.rating == CharacterRating.LEGENDARY:
        user_card_packs.user.moonstone += 250
        user_card_packs.user.save()
    elif user_card_packs.character_card.rating == CharacterRating.HEIRLOOM:
        user_card_packs.user.moonstone += 1000
        user_card_packs.user.save()
    elif user_card_packs.character_card.rating == CharacterRating.EVENT:
        user_card_packs.user.moonstone += 100
        user_card_packs.user.save()

    user_card_packs.delete()

    return JsonResponse({
        "success": True,
    })


@csrf_exempt
@require_http_methods(["POST"])
def set_favorite_card(request):
    json_data = json.loads(request.body)
    user_card_id = json_data.get("userCardId")
    position = json_data.get("position")
    user_card_packs = UserCharacterCard.objects.get(
        id = user_card_id,
    )

    if position == 1:
        user_card_packs.user.favorite_one = user_card_packs.character_card
    elif position == 2:
        user_card_packs.user.favorite_two = user_card_packs.character_card
    elif position == 3:
        user_card_packs.user.favorite_three = user_card_packs.character_card
    user_card_packs.user.save()

    return JsonResponse({
        "success": True,
    })


@csrf_exempt
@require_http_methods(["POST"])
def get_user_by_id(request):
    json_data = json.loads(request.body)
    user_id = json_data.get("userId")
    user = BetaUser.objects.get(pk=user_id)

    favorite_one = None
    favorite_two = None
    favorite_three = None
    if user.favorite_one:
        favorite_one = {
            "id": user.favorite_one.id,
            "card_id": user.favorite_one.id,
            "rating": user.favorite_one.rating,
            "name": user.favorite_one.character.name,
            "serie": user.favorite_one.character.serie.name_en,
            "image_url": user.favorite_one.image.url,
            "type": user.favorite_one.type,
        }
    if user.favorite_two:
        favorite_two = {
            "id": user.favorite_two.id,
            "card_id": user.favorite_two.id,
            "rating": user.favorite_two.rating,
            "name": user.favorite_two.character.name,
            "serie": user.favorite_two.character.serie.name_en,
            "image_url": user.favorite_two.image.url,
            "type": user.favorite_two.type,
        }
    if user.favorite_three:
        favorite_three = {
            "id": user.favorite_three.id,
            "card_id": user.favorite_three.id,
            "rating": user.favorite_three.rating,
            "name": user.favorite_three.character.name,
            "serie": user.favorite_three.character.serie.name_en,
            "image_url": user.favorite_three.image.url,
            "type": user.favorite_three.type,
        }

    user_data = {
        "name": user.username,
        "moonstone": user.moonstone,
        "favorite_one": favorite_one,
        "favorite_two": favorite_two,
        "favorite_three": favorite_three,
    }

    return JsonResponse({
        "user": user_data,
    })


@csrf_exempt
@require_http_methods(["POST"])
def get_all_users(request):
    users = BetaUser.objects.all()

    user_list = []
    for user in users:
        user_list.append({
            "id": user.pk,
            "name": user.username,
        })

    return JsonResponse({
        "users": user_list,
    })
