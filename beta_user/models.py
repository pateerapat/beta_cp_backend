from django.contrib.auth.models import AbstractUser
from django.db import models

from main.models import AbstractModel


class BetaUser(AbstractUser):
    moonstone = models.IntegerField(
        default = 0,
    )
    favorite_one = models.ForeignKey(
        "character_card.CharacterCard",
        related_name    = "favorite_character_card_one",
        on_delete       = models.SET_NULL,
        null            = True,
        blank           = True,
    )
    favorite_two = models.ForeignKey(
        "character_card.CharacterCard",
        related_name    = "favorite_character_card_two",
        on_delete       = models.SET_NULL,
        null            = True,
        blank           = True,
    )
    favorite_three = models.ForeignKey(
        "character_card.CharacterCard",
        related_name    = "favorite_character_card_three",
        on_delete       = models.SET_NULL,
        null            = True,
        blank           = True,
    )


class UserCardPack(AbstractModel):
    user = models.ForeignKey(
        BetaUser,
        related_name    = "card_pack_owned_by",
        on_delete       = models.CASCADE,
    )
    card_pack = models.ForeignKey(
        "card_pack.CardPack",
        related_name    = "card_pack_is_from",
        on_delete       = models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} | {self.card_pack.title}"


class UserCharacterCard(AbstractModel):
    user = models.ForeignKey(
        BetaUser,
        related_name    = "character_card_owned_by",
        on_delete       = models.CASCADE,
    )
    character_card = models.ForeignKey(
        "character_card.CharacterCard",
        related_name    = "character_card_is_from",
        on_delete       = models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} | {self.character_card.character}"
