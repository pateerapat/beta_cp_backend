from django.contrib import admin
from django.urls import (
    path,
    include,
)

from characters import views as CharacterView
from series import views as SerieView

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    # Characters URL Path.
    path(
        "api/characters/",
        CharacterView.CharacterList.as_view(),
    ),
    path(
        "api/characters/<int:pk>",
        CharacterView.CharacterDetail.as_view(),
    ),

    # Series URL Path.
    path(
        "api/series/",
        SerieView.SerieList.as_view(),
    ),
        path(
        "api/series/<int:pk>",
        SerieView.SerieDetail.as_view(),
    ),
]
