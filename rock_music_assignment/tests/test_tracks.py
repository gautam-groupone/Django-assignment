from uuid import UUID

import pytest
from furl import furl
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse


@pytest.mark.django_db
class TestTracks:
    """Test cases for Track API endpoints."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, version):
        self.client = api_client
        self.version = version
        self.track_name = "Last Exit"
        self.track_uuid = UUID("b3083319-47a9-40ed-a4e0-a79d050d9df7")
        self.album_uuid = UUID("b4fee0db-0c93-4470-96b3-cebd158033a0")

    def test_list_tracks(self):
        """Test listing all tracks."""
        url = drf_reverse("track-list", kwargs={"version": self.version})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3695

    def test_search_tracks(self):
        """Test searching tracks by name."""
        url = drf_reverse("track-list", kwargs={"version": self.version})
        url = furl(url).set({"name": self.track_name}).url
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 4
        assert response.data["results"][0]["uuid"] == self.track_uuid

    def test_get_track(self):
        """Test getting a specific track by UUID."""
        url = drf_reverse(
            "track-detail", kwargs={"version": self.version, "uuid": self.track_uuid}
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.track_name
        assert response.data["album"]["uuid"] == self.album_uuid

    def test_track_not_found(self):
        """Test getting a non-existent track returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        url = drf_reverse(
            "track-detail", kwargs={"version": self.version, "uuid": fake_uuid}
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
