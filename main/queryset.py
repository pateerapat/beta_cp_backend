from django.db import models


class BaseQueryset(models.QuerySet):
    class Meta:
        abstract = True
