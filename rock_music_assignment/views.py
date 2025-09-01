from django.views.generic import ListView
from .models import Playlist


class PlaylistListView(ListView):
    model = Playlist
    template_name = 'playlist.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        return (
            Playlist.objects
            .prefetch_related("playlist_tracks__track__album__artist")
            .all()
        )
