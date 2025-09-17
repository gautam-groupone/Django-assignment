from typing import Any

from rest_framework import viewsets, mixins

from .filters import AlbumFilter, ArtistFilter, TrackFilter
from .models import Album, Artist, Track, Playlist
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer, PlaylistSerializer


class BaseAPIViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class ArtistViewSet(BaseAPIViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filterset_class = ArtistFilter


class AlbumViewSet(BaseAPIViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filterset_class = AlbumFilter

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        return queryset.select_related("artist").prefetch_related("tracks")


class TrackViewSet(BaseAPIViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filterset_class = TrackFilter

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        return queryset.select_related("album", "album__artist")


# class PlaylistViewSet(BaseAPIViewSet):
#     queryset = Playlist.objects.all()
#     serializer_class = PlaylistSerializer
#     filterset_class = PlaylistFilter
#
#     def get_queryset(self) -> Any:
#         queryset = super().get_queryset()
#         return queryset
