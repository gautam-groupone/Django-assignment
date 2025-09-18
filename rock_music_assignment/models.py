from typing import Any, Tuple, Union
from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from rock_music_assignment import constants as rock_music_constants


class UUIDManager(models.Manager):
    def get_by_natural_key(self, uuid: str) -> Any:
        return self.get(uuid=uuid)


class UUIDModel(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid4, unique=True)  # type: ignore
    objects = UUIDManager()  # type: ignore

    class Meta:
        abstract = True

    def natural_key(self) -> Tuple[Union[str, int], ...]:
        return (self.uuid,)


class Artist(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The artist name"))  # type: ignore

    class Meta:
        ordering = ("name",)
        indexes = (models.Index(fields=("name",)),)

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        return str(
            reverse(
                "admin:rock_music_assignment_artist_change",
                kwargs={"object_id": self.pk},
            )
        )


class Album(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The album name"))  # type: ignore
    year = models.PositiveSmallIntegerField(  # type: ignore
        help_text=_("The year the album was released")
    )
    artist = models.ForeignKey(  # type: ignore
        Artist,
        help_text=_("The artist that produced the album"),
        related_name="albums",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("artist", "year", "name")
        indexes = (models.Index(fields=("artist", "year", "name")),)

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        return str(
            reverse(
                "admin:rock_music_assignment_album_change",
                kwargs={"object_id": self.pk},
            )
        )


class Track(UUIDModel):
    name = models.CharField(max_length=100, help_text=_("The track name"))  # type: ignore
    album = models.ForeignKey(  # type: ignore
        Album,
        help_text=_("The album this track appears on"),
        related_name="tracks",
        on_delete=models.CASCADE,
    )
    number = models.PositiveSmallIntegerField(  # type: ignore
        help_text=_("The track number on the album")
    )

    class Meta:
        ordering = ("number", "name")
        indexes = (models.Index(fields=("number", "name")),)
        constraints = (
            models.UniqueConstraint(
                fields=("album", "number"), name="unique_album_number"
            ),
        )

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        return str(
            reverse(
                "admin:rock_music_assignment_track_change",
                kwargs={"object_id": self.pk},
            )
        )


# Playlist Tracks related changes #
class Playlist(UUIDModel):
    "Playlist models to store playlists"
    name = models.CharField(
        max_length=rock_music_constants.CHAR_FIELD_MAX_SIZE,
        help_text=rock_music_constants.HELP_TEXTS['PLAYLIST_NAME']
    )
    tracks = models.ManyToManyField(
        to=Track, through="PlayListTrack", related_name="playlist_tracks"
    )


class PlayListTrack(UUIDModel):
    track_id = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        help_text=rock_music_constants.HELP_TEXTS['TRACK']
    )
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        help_text=rock_music_constants.HELP_TEXTS['PLAYLIST']
    )
    order = models.IntegerField(
        help_text=rock_music_constants.HELP_TEXTS['ORDER']
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("order", "playlist_id", "track_id"), name="unique_track_order_in_playlist"
            ),
        )
    
    def __str__(self):
        return f'{self.playlist_id} - {self.track_id_id} - {self.order}'
