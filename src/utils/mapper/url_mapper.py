from src.data.models.url import Url


class UrlMapper:

    @staticmethod
    def to_dict(url: Url):
        return {
            "shortened_url": url.shortened_url,
            "original_url": url.original_url,
            "created_at": url.created_at,
            "expires_at": url.expires_at,
        }

    @staticmethod
    def from_dict(data: Url):
        return Url(
            shortened_url=data["shortened_url"],
            original_url=data["original_url"],
            created_at=data.get('created_at'),
        )