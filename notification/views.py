import json
from django.utils.timezone import timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from beta_user.models import (
    BetaUser,
    UserCardPack,
)
from character_card.models import CharacterRating

from .models import Notification


@csrf_exempt
@require_http_methods(["POST"])
def get_all_notification(request):
    notifications = Notification.objects.all().order_by("-created")[:20]
    notification_list = []
    for notification in notifications:
        color = '#828385'
        if notification.character_card.rating == CharacterRating.COMMON:
            color = '#828385'
        elif notification.character_card.rating == CharacterRating.UNCOMMON:
            color = '#00A386'
        elif notification.character_card.rating == CharacterRating.RARE:
            color = '#2471A3'
        elif notification.character_card.rating == CharacterRating.EPIC:
            color = '#7D3C98'
        elif notification.character_card.rating == CharacterRating.LEGENDARY:
            color = '#F1C40F'
        elif notification.character_card.rating == CharacterRating.HEIRLOOM:
            color = '#FF392E'
        elif notification.character_card.rating == CharacterRating.EVENT:
            color = '#DC2367'
        notification.created += timedelta(hours=7)
        notification_list.append({
            "card_pack_name": notification.card_pack.title,
            "username": notification.user.username,
            "character_name": notification.character_card.character.name,
            "character_rating": notification.character_card.rating,
            "character_type": notification.character_card.type,
            "character_image": notification.character_card.image.url,
            "rating_color": color,
            "time": notification.created.strftime("%d/%m/%Y, %H:%M:%S"),
        })

    return JsonResponse({
        "notifications": notification_list,
    })
