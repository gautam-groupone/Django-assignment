from typing import Any

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny

from .filters import AlbumFilter, ArtistFilter, TrackFilter
from .models import Album, Artist, Track, Playlist
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer, PlayListCreateUpdateDeleteSerializer, PlayListOrderUpdateSerializer


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


class PlayListCreateUpdateDeleteViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlayListCreateUpdateDeleteSerializer

    def get_seriaizer_context(self):
        context = super().get_serializer_context()
        context['playlist_id'] = self.request.get('pk')
        return context


class PlaylistOrderUpdateAPI(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlayListOrderUpdateSerializer
    pk_url_kwarg = 'playlist__uuid'
    lookup_url_kwarg = 'playlist__uuid'
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_object(self):
        print(self.kwargs)
        return self.queryset.get(uuid=self.kwargs.get('playlist__uuid'))
    