from django.db import models

from main.queryset import BaseQueryset


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    updated = models.DateTimeField(
        auto_now        = True,
        editable        = False,
        null            = True,
    )
    created = models.DateTimeField(
        auto_now_add    = True,
        editable        = False,
    )
    objects = BaseQueryset.as_manager()
