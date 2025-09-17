from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Playlist, TrackPlaylistLink


class AllPlaylistView(APIView):
    data = None
    ctx = {}

    def get(self, request, *args, **kwargs):
        """
        This method will return all the playlists
        """
        queryset = Playlist.objects.all().values('id', 'name')
        return Response({'status': 'ok', 'msg': 'Data fetched successfully!', 'data': list(queryset)})

    def post(self, request, *args, **kwargs):
        self.data = request.data
        print(self.data)
        name = self.data.get('name', '').strip()
        if not name:
            self.ctx = {'status': 'error', 'msg': 'Name of the playlist cannot be empty!'}
            return Response(self.ctx)
        if Playlist.objects.filter(name__iexact=name):
            self.ctx = {'status': 'error', 'msg': 'Playlist with same name already exists!'}
            return Response(self.ctx)

        playlist_obj = Playlist(name=name)
        playlist_obj.save()
        self.ctx = {'status': 'ok', 'msg': 'Playlist successfully created!'}
        return Response(self.ctx)


class SinglePlaylistView(APIView):
    ctx = None
    data = None

    def get(self, request, *args, **kwargs):
        data = []
        playlist_id = kwargs.get('id')
        playlist_obj = Playlist.objects.filter(id=playlist_id).first()
        if playlist_obj is None:
            ctx = {'status': 'error', 'msg': 'Playlist not found!', 'data': data}
        else:
            playlist_tracks = TrackPlaylistLink.objects.select_related('track').filter(
                playlist_id=playlist_obj.id).order_by('track_order')
            for track_ in playlist_tracks:
                data.append({
                    'id': track_.track_id,
                    'name': track_.track.name,
                    'order_num': track_.track_order
                })
            ctx = {'status': 'ok', 'msg': 'Data fetched successfully!', 'data': data}
        return Response(ctx)

    def post(self, request, *args, **kwargs):
        self.ctx = {}
        self.data = request.data
        action = int(self.data['action'])
        action_mapper = {
            1: self.update_playlist,
            2: self.remove_track_from_playlist,
            3: self.delete_playlist,
        }
        status = action_mapper.get(action, lambda: 'Invalid')()
        # if not status:
        #     return Response({'status': 'error', 'msg': 'Something went wrong!'})
        return Response(self.ctx)

    def update_playlist(self):
        name = self.data.get('name', '').strip()
        playlist_id = self.data.get('playlist_id', '')
        track_id = self.data.get('track_id', None)
        track_order = self.data.get('track_order', 0)
        if not playlist_id:  # Case where empty string is being received or no key of playlist id
            self.ctx = {'status': 'error', 'msg': 'Provide a valid playlist!'}
            return
        playlist_obj = Playlist.objects.filter(id=playlist_id).first()
        if playlist_obj is None:
            self.ctx = {'status': 'error', 'msg': 'Playlist not found!'}
            return
        if not name:
            self.ctx = {'status': 'error', 'msg': 'Name of the playlist cannot be empty!'}
            return
        playlist_obj.name = name
        playlist_obj.save()

        if track_id:
            playlist_track_link = TrackPlaylistLink.objects.filter(playlist_id=playlist_obj.pk,
                                                                   track_id=track_id).first()
            if playlist_track_link is None and TrackPlaylistLink.objects.filter(
                    playlist_id=playlist_obj.pk).count() >= 100:
                self.ctx = {'status': 'error', 'msg': 'Limit to add tracks reached!'}
                return

            if playlist_track_link:
                playlist_track_link.track_order = track_order
            else:
                playlist_track_link = TrackPlaylistLink(playlist_id=playlist_obj.id, track_id=track_id,
                                                        track_order=track_order)
            playlist_track_link.save()

            # iterated_tracks = set()
            # playlist_track_links = TrackPlaylistLink.objects.filter(playlist_id=playlist_obj.pk,
            #                                                         track_id__in=list(track_data.keys()))
            # links_to_update = []
            # for link in playlist_track_links:
            #     link.track_order = track_data.get(int(link.track_id))
            #     links_to_update.append(link)
            #     iterated_tracks.add(link.track_id)
            #
            # track_ids_to_add = set(track_data.keys()) - iterated_tracks
            # links_to_create = []
            # for track_id in track_ids_to_add:
            #     links_to_create.append(
            #         TrackPlaylistLink(track_id=track_id,
            #                           track_order=track_data.get(track_id),
            #                           playlist_id=playlist_obj.pk
            #                           )
            #     )
            #
            # TrackPlaylistLink.objects.bulk_update(links_to_update, ['track_order'])
            # TrackPlaylistLink.objects.bulk_create(links_to_create)

        self.ctx = {'status': 'ok', 'msg': f'{playlist_obj.name} updated successfully!'}

    def remove_track_from_playlist(self):
        """
        This method will remove a track from the playlist
        """
        playlist_id = self.data.get('playlist_id', '')
        track_id = self.data.get('track_id', None)
        if not playlist_id:  # Case where empty string is being received or no key of playlist id
            self.ctx = {'status': 'error', 'msg': 'Provide a valid playlist!'}
            return
        playlist_obj = Playlist.objects.filter(pk=playlist_id).first()
        if playlist_obj is None:
            self.ctx = {'status': 'error', 'msg': 'Playlist not found!'}
            return

        link_obj = TrackPlaylistLink.objects.filter(track_id=track_id, playlist_id=playlist_obj.pk).first()
        if link_obj is None:
            self.ctx = {'status': 'error', 'msg': 'Track not found in the playlist!'}
            return
        link_obj.delete()
        self.ctx = {'status': 'ok', 'msg': 'Track removed successfully!'}

    def delete_playlist(self):
        playlist_id = self.data.get('playlist_id', '')
        if not playlist_id:  # Case where empty string is being received or no key of playlist id
            self.ctx = {'status': 'error', 'msg': 'Provide a valid playlist!'}
            return
        playlist_obj = Playlist.objects.filter(pk=playlist_id).first()
        if playlist_obj is None:
            self.ctx = {'status': 'error', 'msg': 'Playlist not found!'}
            return
        name = playlist_obj.name
        playlist_obj.delete()

        self.ctx = {'status': 'ok', 'msg': f'{name} deleted successfully!'}