from typing import Any

from rest_framework import viewsets

from .filters import AlbumFilter, ArtistFilter, TrackFilter, PlaylistFilter, TrackPlaylistOrderFilter
from .models import Album, Artist, Track, Playlist, TrackPlaylistOrder
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer, PlaylistSerializer, \
    TrackPlaylistOrderSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError


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


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    filterset_class = PlaylistFilter
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class TrackPlaylistOrderViewSet(viewsets.ModelViewSet):
    queryset = TrackPlaylistOrder.objects.all()
    serializer_class = TrackPlaylistOrderSerializer
    filterset_class = TrackPlaylistOrderFilter
    lookup_field = "id"

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        return queryset.select_related("playlist", "track")

    def perform_create(self, serializer):
        playlist_uuid = self.request.data.get("playlist_uuid")
        track_uuid = self.request.data.get("track_uuid")

        playlist = get_object_or_404(Playlist, uuid=playlist_uuid)
        if playlist.tracks.count() >= 100:
            raise ValidationError("A playlist cannot have more than 100 tracks.")

        track = get_object_or_404(Track, uuid=track_uuid)
        if not track.album:
            raise ValidationError("Track must belong to an album.")

        if TrackPlaylistOrder.objects.filter(playlist=playlist, track=track).exists():
            raise ValidationError("This track is already in the playlist.")

        serializer.save(playlist=playlist, track=track)
