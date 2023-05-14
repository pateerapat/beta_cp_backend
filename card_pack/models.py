from django.db import models
from multiselectfield import MultiSelectField

from character_card.models import CharacterRating
from main.models import AbstractModel


class CardPack(AbstractModel):
    title = models.CharField(
        max_length  = 512,
        default     = "",
    )
    include_ratings = MultiSelectField(
        max_length  = 32,
        choices     = CharacterRating.CHOICES,
    )
    include_character_cards = models.ManyToManyField(
        "character_card.CharacterCard",
        related_name    = "included_character_cards",
        blank           = True,
    )
    ratings_rule = models.CharField(
        max_length  = 512,
        default     = "",
    )
    include_series = models.ManyToManyField(
        "series.Serie",
        related_name    = "included_series",
        blank           = True,
    )
    is_active = models.BooleanField(
        default = True,
    )
    is_by_series = models.BooleanField(
        default = False,
    )
    is_by_event = models.BooleanField(
        default = False,
    )
    is_new = models.BooleanField(
        default = True,
    )
    description = models.TextField(
        max_length  = 1024,
        default     = "",
    )
    price = models.IntegerField(
        default = 0,
    )
    image = models.FileField(
        upload_to   = "card_pack_images",
    )

    def __str__(self):
        return self.title
