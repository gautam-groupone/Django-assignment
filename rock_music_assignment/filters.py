from django_filters import rest_framework as filters

from .models import Album, Artist, Track, Playlist, TrackPlaylistOrder


class ArtistFilter(filters.FilterSet):

    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Artist
        fields = ("name",)


class AlbumFilter(filters.FilterSet):

    artist_uuid = filters.UUIDFilter("artist__uuid")
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Album
        fields = ("artist_uuid", "name")


class TrackFilter(filters.FilterSet):

    album_uuid = filters.UUIDFilter("album__uuid")
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Track
        fields = ("album_uuid", "name")


class PlaylistFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Playlist
        fields = ("name", )


class TrackPlaylistOrderFilter(filters.FilterSet):
    playlist_uuid = filters.UUIDFilter("playlist__uuid")
    track_uuid = filters.UUIDFilter("track__uuid")

    class Meta:
        model = TrackPlaylistOrder
        fields = ("playlist_uuid", "track_uuid")
