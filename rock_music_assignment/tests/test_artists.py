from uuid import UUID

import pytest
from furl import furl
from rest_framework import status
from rest_framework.reverse import reverse as drf_reverse


@pytest.mark.django_db
class TestArtists:
    """Test cases for Artist API endpoints."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, version):
        self.client = api_client
        self.version = version
        self.artist_name = "Pearl Jam"
        self.artist_uuid = UUID("9e52205f-9927-4eff-b132-ce10c6f3e0b1")

    def test_list_artists(self):
        """Test listing all artists."""
        url = drf_reverse("artist-list", kwargs={"version": self.version})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_search_artists(self):
        """Test searching artists by name."""
        url = drf_reverse("artist-list", kwargs={"version": self.version})
        url = furl(url).set({"name": self.artist_name}).url
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["uuid"] == self.artist_uuid

    def test_get_artist(self):
        """Test getting a specific artist by UUID."""
        url = drf_reverse(
            "artist-detail", kwargs={"version": self.version, "uuid": self.artist_uuid}
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.artist_name

    def test_artist_not_found(self):
        """Test getting a non-existent artist returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        url = drf_reverse(
            "artist-detail", kwargs={"version": self.version, "uuid": fake_uuid}
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
