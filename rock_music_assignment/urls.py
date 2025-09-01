from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from .viewsets import AlbumViewSet, ArtistViewSet, TrackViewSet, PlaylistViewSet, TrackPlaylistOrderViewSet
from .views import PlaylistListView

urlpatterns = []


if settings.DJANGO_ADMIN_ENABLED:
    urlpatterns += [
        re_path("^$", RedirectView.as_view(url="/admin/", permanent=True)),
        path("admin/", admin.site.urls),
    ]

if settings.DJANGO_API_ENABLED:
    api_router = DefaultRouter(trailing_slash=False)
    api_router.register("artists", ArtistViewSet)
    api_router.register("albums", AlbumViewSet)
    api_router.register("tracks", TrackViewSet)
    api_router.register("playlists", PlaylistViewSet)
    api_router.register("playlist-tracks", TrackPlaylistOrderViewSet)

    urlpatterns += [
        path("api/<version>/", include(api_router.urls)),
        path("list_playlist/", PlaylistListView.as_view(), name="playlist_list")
    ]
