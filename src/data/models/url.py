from datetime import datetime, timedelta
class Url:
    def __init__(self, url_id, original_url, shortened_url, created_at, expires_at):
        self.original_url = original_url
        self.shortened_url = shortened_url
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(days=5)