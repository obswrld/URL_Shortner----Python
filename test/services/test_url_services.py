import pytest
import mongomock
from datetime import datetime, timedelta
from src.data.models.url import Url
from src.data.repositories.url_repositories import UrlRepository
from src.service.url_service import UrlService

class TestUrlService:

    @pytest.fixture(autouse=True)
    def setup(self):
        mock_client = mongomock.MongoClient()
        mock_db = mock_client['test_db']
        mock_collection = mock_db['test_collection']

        self.url_repository = UrlRepository(collection=mock_collection)
        self.service = UrlService(url_repository=self.url_repository)


    def test_shorten_url_and_get_original_url(self):
        original_url = "http://example.com"
        short_url = self.service.shorten_url(original_url)
        assert short_url["original_url"] == original_url
        assert "shortened_url" in short_url
        assert isinstance(short_url["shortened_url"], str)
        result = self.service.get_original_url(short_url["shortened_url"])
        assert result["original_url"] == original_url

    def test_get_shortened_url(self):
        original_url = "http://example.com"
        shortened_data = self.service.shorten_url(original_url)
        shortened_code = shortened_data["shortened_url"]
        retrieve = self.service.get_shortened_url(shortened_code)
        assert retrieve is not None
        assert retrieve["shortened_url"] == shortened_code
        assert retrieve["original_url"] == original_url

    def test_delete_shortened_url(self):
        original_url = "http://example.com"
        shortened_data = self.service.shorten_url(original_url)
        shortened_code = shortened_data["shortened_url"]
        delete = self.service.delete_shortened_url(shortened_code)
        assert delete is True
        after_delete = self.service.get_shortened_url(shortened_code)
        assert after_delete is None
