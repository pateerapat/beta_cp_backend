from django.contrib import admin

from .models import (
    BetaUser,
    UserCardPack,
    UserCharacterCard,
)

admin.site.register([BetaUser, UserCharacterCard, UserCardPack])

