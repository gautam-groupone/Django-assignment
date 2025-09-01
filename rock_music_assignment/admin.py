from django.contrib import admin

from .models import Album, Artist, Track, Playlist, TrackPlaylistOrder

# Basic admin registration without type hints
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Playlist)
admin.site.register(TrackPlaylistOrder)
