from django.db import models

from main.models import AbstractModel


class CharacterRating:
    COMMON      = "common"
    UNCOMMON    = "uncommon"
    RARE        = "rare"
    EPIC        = "epic"
    LEGENDARY   = "legendary"
    HEIRLOOM    = "heirloom"
    EVENT       = "event"

    CHOICES = [
        (COMMON,    "Common"),
        (UNCOMMON,  "Uncommon"),
        (RARE,      "Rare"),
        (EPIC,      "Epic"),
        (LEGENDARY, "Legendary"),
        (HEIRLOOM,  "Heirloom"),
        (EVENT,     "Event"),
    ]


class Character(AbstractModel):
    serie = models.ForeignKey(
        "series.Serie",
        related_name    = "belong_to_serie",
        on_delete       = models.CASCADE,
        null            = True,
        blank           = True,
    )
    name = models.CharField(
        max_length  = 512,
        default     = "",
    )
    rating = models.CharField(
        max_length  = 32,
        choices     = CharacterRating.CHOICES,
        default     = CharacterRating.COMMON,
    )
    image = models.FileField(
        upload_to   = "media/character_images",
    )

    def __str__(self):
        return self.name
