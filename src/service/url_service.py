from src.data.models.url import Url
from src.data.repositories.url_repositories import UrlRepository
from src.utils.mapper.url_mapper import UrlMapper
import random
import string

class UrlService:
    def __init__(self, url_repository=None):
        self.url_repository = url_repository if url_repository else UrlRepository()

    @staticmethod
    def generate_short_url(length: int = 6):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def shorten_url(self, original_url: str):
        short_url = self.generate_short_url()
        url_obj = Url(original_url=original_url, shortened_url=short_url)

        self.url_repository.save(url_obj)

        return UrlMapper.to_dict(url_obj)

    def get_shortened_url(self, shortened_url: str):
        short_url = self.url_repository.find_by_shortened_url(shortened_url)
        if short_url:
            return UrlMapper.to_dict(short_url)
        return None

    def get_original_url(self, shortened_url: str):
        short_url = self.url_repository.find_by_shortened_url(shortened_url)
        if short_url:
            return UrlMapper.to_dict(short_url)
        return None

    def delete_shortened_url(self, shortened_url: str):
        return self.url_repository.delete_by_shortened_url(shortened_url)

    def clean_expired_url(self):
        return self.url_repository.delete_expired_url()

