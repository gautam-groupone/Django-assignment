from uuid import UUID

import pytest
from furl import furl
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse


@pytest.mark.django_db
class TestAlbums:
    """Test cases for Album API endpoints."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, version):
        self.client = api_client
        self.version = version
        self.album_name = "Vitalogy"
        self.album_uuid = UUID("b4fee0db-0c93-4470-96b3-cebd158033a0")
        self.artist_uuid = UUID("9e52205f-9927-4eff-b132-ce10c6f3e0b1")

    def test_list_albums(self):
        """Test listing all albums."""
        url = drf_reverse("album-list", kwargs={"version": self.version})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 291

    def test_search_albums(self):
        """Test searching albums by name."""
        url = drf_reverse("album-list", kwargs={"version": self.version})
        url = furl(url).set({"name": self.album_name}).url
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        assert response.data["results"][0]["uuid"] == self.album_uuid
        assert response.data["results"][0]["artist"]["uuid"] == self.artist_uuid

    def test_get_album(self):
        """Test getting a specific album by UUID."""
        url = drf_reverse(
            "album-detail", kwargs={"version": self.version, "uuid": self.album_uuid}
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.album_name
        assert response.data["artist"]["uuid"] == self.artist_uuid

    def test_album_not_found(self):
        """Test getting a non-existent album returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        url = drf_reverse(
            "album-detail", kwargs={"version": self.version, "uuid": fake_uuid}
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
