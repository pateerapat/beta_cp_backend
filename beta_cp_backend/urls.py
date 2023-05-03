from knox import views as knox_views

from django.contrib import admin
from django.urls import path

from .views import (
    LoginAPI,
    RegisterAPI,
    UserAPI,
)

from characters import views as CharacterView
from series import views as SerieView


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "api/register/",
        RegisterAPI.as_view(),
        name="register",
    ),
    path(
        "api/login/",
        LoginAPI.as_view(),
        name="login",
    ),
    path(
        "api/user/",
        UserAPI.as_view(),
        name="user",
    ),
    path(
        "api/logout/",
        knox_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "api/logoutall/",
        knox_views.LogoutAllView.as_view(),
        name="logoutall",
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
