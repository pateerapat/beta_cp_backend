from django.db import models

from main.models import AbstractModel


class CharacterRating:
    # Rating Rule.
    COMMON      = "common"      # 0.90
    UNCOMMON    = "uncommon"    # 0.05
    RARE        = "rare"        # 0.03
    EPIC        = "epic"        # 0.01
    LEGENDARY   = "legendary"   # 0.008
    HEIRLOOM    = "heirloom"    # 0.002
    EVENT       = "event"       # 0.01

    CHOICES = [
        (COMMON,    "Common"),
        (UNCOMMON,  "Uncommon"),
        (RARE,      "Rare"),
        (EPIC,      "Epic"),
        (LEGENDARY, "Legendary"),
        (HEIRLOOM,  "Heirloom"),
        (EVENT,     "Event"),
    ]


class CharacterCard(AbstractModel):
    rating = models.CharField(
        max_length  = 32,
        choices     = CharacterRating.CHOICES,
        default     = CharacterRating.COMMON,
    )
    character = models.ForeignKey(
        "characters.Character",
        related_name    = "belong_to_character",
        on_delete       = models.CASCADE,
        null            = True,
        blank           = True,
    )
    type = models.CharField(
        max_length  = 64,
        default     = "",
    )
    image = models.FileField(
        upload_to   = "character_images",
    )

    def __str__(self):
        return f"{self.character.name} | {self.rating}" if self.character else self.pk
