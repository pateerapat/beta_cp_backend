from django.db import models

from main.models import AbstractModel


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

    def __str__(self):
        return self.name
