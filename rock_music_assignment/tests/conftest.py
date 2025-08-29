import pytest
from django.conf import settings
from django.core.management import call_command
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Setup database for all tests."""
    with django_db_blocker.unblock():
        # Load fixtures for all tests
        call_command("loaddata", "rock_music_assignment/fixtures/initial_data.json")


@pytest.fixture
def api_client():
    """Provide an API client for testing."""
    return APIClient()


@pytest.fixture
def version():
    """Provide the API version for testing."""
    return settings.REST_FRAMEWORK["DEFAULT_VERSION"]


@pytest.fixture
def album_data():
    """Provide test album data."""
    return {
        "album_name": "Vitalogy",
        "album_uuid": "b4fee0db-0c93-4470-96b3-cebd158033a0",
        "artist_uuid": "9e52205f-9927-4eff-b132-ce10c6f3e0b1",
    }


@pytest.fixture
def artist_data():
    """Provide test artist data."""
    return {
        "artist_name": "Pearl Jam",
        "artist_uuid": "9e52205f-9927-4eff-b132-ce10c6f3e0b1",
    }


@pytest.fixture
def track_data():
    """Provide test track data."""
    return {
        "track_name": "Last Exit",
        "track_uuid": "b3083319-47a9-40ed-a4e0-a79d050d9df7",
        "album_uuid": "b4fee0db-0c93-4470-96b3-cebd158033a0",
    }


@pytest.fixture
def playlist_data():
    """Provide test playlist data."""
    return {
        "playlist_name": "My Favorites",
        "playlist_uuid": "d4fee0db-0c93-4470-96b3-cebd158033a0",
    }
