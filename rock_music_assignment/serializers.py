from furl import furl
from rest_framework import serializers
from rest_framework.reverse import reverse as drf_reverse

from django.db.models import Q

from .fields import UUIDHyperlinkedIdentityField
from .models import Album, Artist, Track, Playlist, PlayListTrack
from rock_music_assignment import constants as rock_music_assigments_constants
from manager_utils import bulk_upsert


class TrackAlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name")


class TrackAlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="album-detail")
    artist = TrackAlbumArtistSerializer()

    class Meta:
        model = Album
        fields = ("uuid", "url", "name", "artist")


class TrackSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="track-detail")
    album = TrackAlbumSerializer()

    class Meta:
        model = Track
        fields = ("uuid", "url", "name", "number", "album")


class AlbumTrackSerializer(TrackSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="track-detail")

    class Meta:
        model = Track
        fields = ("uuid", "url", "name", "number")


class AlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name")


class AlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="album-detail")
    artist = AlbumArtistSerializer()
    tracks = AlbumTrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ("uuid", "url", "name", "year", "artist", "tracks")


class ArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")
    albums_url = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name", "albums_url")

    def get_albums_url(self, artist: Artist) -> str:
        path = drf_reverse("album-list", request=self.context["request"])
        return str(furl(path).set({"artist_uuid": artist.uuid}).url)


class PlayListCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    track_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )

    def _validate_track_ids(self, value):
        """Check for duplicate tracks and max track count in a playlist"""
        # check for duplicates
        if PlayListTrack.objects.filter(
            track_id__in=value or [],
            playlist_id=self.context['playlist_id']
        ).count():
            raise serializers.ValidationError(
                rock_music_assigments_constants.ERRORS['DUPLICATES_TRACKS']
            )
        
        # check if total count is less than 100
        if PlayListTrack.objects.filter(
            playlist_id=self.context['playlist_id']
        ).count() + len(value) > rock_music_assigments_constants.MAX_TRACK_COUNT:
            raise serializers.ValidationError(
                rock_music_assigments_constants.ERRORS['DUPLICATES_TRACKS']
            )
    
        return value

    def _create_playlist_tracks(self, track_ids, is_update: bool = False):
        curr_order = PlayListTrack.objects.filter(
            playlist_id=self.instance.id
        ).count() + 1 if is_update else 1
        playlist_track_objects = []
        for track_id in track_ids:
            curr_order += 1
            playlist_track_objects.append(PlayListTrack(
                playlist_id=self.instance.id,
                track_id=track_id,
                order=curr_order
            ))

        if playlist_track_objects:
            PlayListTrack.objects.bulk_create(playlist_track_objects)
        

    def create(self, validated_data):
        track_ids = validated_data.pop('track_ids', [])
        playlist = super().create(validated_data)
        self._create_playlist_tracks(track_ids=track_ids)
        return playlist
    
    def update(self, validated_data):
        if not (validated_data.get('name') or  validated_data.get('track_ids')):
            return
        
        tracks_to_be_added = validated_data.pop('track_ids', [])
        if tracks_to_be_added:
            self._validate_track_ids(tracks_to_be_added)
            self._create_playlist_tracks(track_ids=tracks_to_be_added, is_update=True)
            
        return super().update(validated_data)

    class Meta:
        model = Playlist
        fields = ("uuid", "name", "track_ids")


class TrackInfoSerializer(serializers.Serializer):
    track_id = serializers.UUIDField()
    updated_order = serializers.IntegerField()
    curr_order = serializers.IntegerField()


class PlayListOrderUpdateSerializer(serializers.Serializer):
    track_info = TrackInfoSerializer(source='*')

    class Meta:
        fields = ("track_info")
    
    def _validate_track_info(self, value):
        if not PlayListTrack.objects.filter(
            track_id=value['track_id'],
            playlist_id=self.context['playlist_id'],
            order=value['curr_order']
        ).exists():
            raise serializers.ValidationError(
                rock_music_assigments_constants.ERRORS['PLAYLIST_TRACK_NOT_FOUND']
            )

        return value

    def update(self, instance, validated_data):
        print(validated_data)
        track_info = {
            'updated_order': validated_data['updated_order'],
            'curr_order': validated_data['curr_order'],
            'track_id': validated_data['track_id'],
        }
        track_filter_qs = None
        if track_info['updated_order'] > track_info['curr_order']:
            track_filter_qs = Q(
                order__gte=track_info['curr_order'],
                order__lte=track_info['updated_order']
            )
        else:
            track_filter_qs = Q(
                order__lte=track_info['curr_order'],
                order__gte=track_info['updated_order']
            )

        tracks_to_update = PlayListTrack.objects.filter(
            track_filter_qs, playlist_id=instance.id
        ).order_by('order')
        updated_tracks = []
        for track in tracks_to_update:
            if track.order == max(track_info['curr_order'], track_info['updated_order']):
                track.order = int(min(track_info['curr_order'], track_info['updated_order']))
            else:
                track.order = track.order + 1
            
            updated_tracks.append(track)
        
        if updated_tracks:
            bulk_upsert(
                PlayListTrack.objects.filter(track_filter_qs, playlist_id=instance.id),
                updated_tracks,
                ['uuid'],
                ['order']
            )
        
        return validated_data
