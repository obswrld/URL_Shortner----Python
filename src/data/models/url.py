from datetime import datetime, timedelta
class Url:
    def __init__(self, original_url, shortened_url, created_at=None, expires_at=None, url_id=None):
        self.url_id = url_id
        self.original_url = original_url
        self.shortened_url = shortened_url
        self.created_at = created_at or datetime.now()
        self.expires_at = expires_at or (self.created_at + timedelta(days=5))

    def to_dict(self):
        return {
            "url_id": self.url_id,
            "original_url": self.original_url,
            "shortened_url": self.shortened_url,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
        }