import pytest
import mongomock
from src.data.models.url import Url
from src.data.repositories.url_repositories import UrlRepository
from datetime import datetime, timedelta

@pytest.fixture
def mock_collection():
    return mongomock.MongoClient().db.collection

@pytest.fixture
def url_repository(mock_collection):
    return UrlRepository(collection=mock_collection)

def test_save_and_find_by_shortened_url(url_repository):
    url = Url(
        shortened_url="123rew",
        original_url="https://example.com",
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(days=5),
        url_id=None
    )
    inserted_id = url_repository.save(url)
    assert inserted_id is not None
    found_url = url_repository.find_by_shortened_url("123rew")
    assert found_url is not None
    assert found_url.original_url == "https://example.com"
    assert found_url.shortened_url == "123rew"


def test_find_by_original_url(url_repository):
    url = Url(
        shortened_url="123rew",
        original_url="https://example.com",
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(days=5),
        url_id=None
    )
    inserted_id = url_repository.save(url)
    assert inserted_id is not None

    found_url = url_repository.find_by_original_url("https://example.com")
    assert found_url is not None
    assert found_url.original_url == "https://example.com"
    assert found_url.shortened_url == "123rew"

def test_delete_by_shortened_url(url_repository):
    url = Url(
        shortened_url="123rew",
        original_url="https://example.com",
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(days=5),
        url_id=None
    )
    inserted_id = url_repository.save(url)
    assert inserted_id is not None
    delete_url = url_repository.delete_by_shortened_url("123rew")
    assert delete_url is True

def test_delete_by_original_url(url_repository):
    url = Url(
        shortened_url="123rew",
        original_url="https://example.com",
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(days=5),
        url_id=None
    )
    inserted_id = url_repository.save(url)
    assert inserted_id is not None
    delete_url = url_repository.delete_by_original_url("https://example.com")
    assert delete_url is True

def test_delete_expired_url(url_repository):
    expired_url = Url(
        shortened_url="123rew",
        original_url="https://example.com",
        created_at=datetime.now() - timedelta(days=10),
        expires_at=datetime.now() - timedelta(days=5),
        url_id=None
    )

    valid_url = Url(
        shortened_url="123rew",
        original_url="https://example.com",
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(days=5),
        url_id=None
    )
    url = url_repository.save(expired_url)
    url1 = url_repository.save(valid_url)

    deleted_url = url_repository.delete_expired_url()
    assert deleted_url == 1
