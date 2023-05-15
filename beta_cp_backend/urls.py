from knox import views as knox_views

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from .views import (
    LoginAPI,
    RegisterAPI,
    UserAPI,
)


from beta_cp_backend import settings
from beta_user import views as UserView
from characters import views as CharacterView
from character_card import views as CharacterCardView
from card_pack import views as CardPackView
from series import views as SerieView
from notification import views as NotificationView


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
        "api/user/<int:pk>",
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

    # Series URL Path.
    path(
        "api/character_packs/",
        CharacterCardView.CharacterCardList.as_view(),
    ),
        path(
        "api/character_packs/<int:pk>",
        CharacterCardView.CharacterCardDetail.as_view(),
    ),

    # Series URL Path.
    path(
        "api/card_packs/",
        CardPackView.CardPackList.as_view(),
    ),
        path(
        "api/card_packs/<int:pk>",
        CardPackView.CardPackDetail.as_view(),
    ),

    # Custom Path.
    path(
        "api/user_character_cards/",
        UserView.get_user_character_cards,
        name="get_user_character_cards",
    ),
    path(
        "api/user_card_packs/",
        UserView.get_user_card_packs,
        name="get_get_user_card_packs",
    ),
    path(
        "api/shop_card_packs/",
        CardPackView.get_shop_card_packs,
        name="get_shop_card_packs",
    ),
    path(
        "api/purchase_pack/",
        CardPackView.purchase_pack,
        name="purchase_pack",
    ),
    path(
        "api/open_pack/",
        CardPackView.open_pack,
        name="open_pack",
    ),
    path(
        "api/get_all_character_cards/",
        CharacterCardView.get_all_character_cards,
        name="get_all_character_cards",
    ),
    path(
        "api/sell_user_card/",
        UserView.sell_user_card,
        name="sell_user_card",
    ),
    path(
        "api/get_all_notification/",
        NotificationView.get_all_notification,
        name="get_all_notification",
    ),
    path(
        "api/set_favorite_card/",
        UserView.set_favorite_card,
        name="set_favorite_card",
    ),
    path(
        "api/get_user_by_id/",
        UserView.get_user_by_id,
        name="get_user_by_id",
    ),
    path(
        "api/get_all_users/",
        UserView.get_all_users,
        name="get_all_users",
    ),
]

urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
