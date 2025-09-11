from typing import Any
from rest_framework import viewsets

from .filters import AlbumFilter, ArtistFilter, TrackFilter
from .models import Album, Artist, Track
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer


class BaseAPIViewSet(viewsets.ReadOnlyModelViewSet):
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
