from django.db import models

from main.models import AbstractModel


class Serie(AbstractModel):
    reversed_line = [
        "serie_characters",
    ]
    name_en = models.CharField(
        max_length  = 512,
        default     = "",
    )
    name_jp = models.CharField(
        max_length  = 512,
        default     = "",
    )

    def __str__(self):
        return self.name_en
