from django.db import models

from main.models import AbstractModel


class Notification(AbstractModel):
    user = models.ForeignKey(
        "beta_user.BetaUser",
        related_name    = "notification_by",
        on_delete       = models.CASCADE,
    )
    card_pack = models.ForeignKey(
        "card_pack.CardPack",
        related_name    = "notification_card_pack",
        on_delete       = models.CASCADE,
    )
    character_card = models.ForeignKey(
        "character_card.CharacterCard",
        related_name    = "notification_character_card",
        on_delete       = models.CASCADE,
    )
