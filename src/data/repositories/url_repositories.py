from src.config.config import url_collection
from src.data.models.url import Url
from pymongo.errors import PyMongoError
# from bson.objectid import ObjectId
from datetime import datetime

class UrlRepository:
    def __init__(self, collection=url_collection):
        self.collection = collection

    def save(self, url: Url):
        try:
            data = url.to_dict()
            print("Saving to MongoDB:", data)
            result = self.collection.insert_one(data)
            print("Inserted ID:", result.inserted_id)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Error saving URL: {e}")
            return None

    def find_by_shortened_url(self, shortened_url: str) -> Url:
        try:
            print("Finding Url by shortened url:", shortened_url)
            url_date = self.collection.find_one({"shortened_url": shortened_url})
            print("found: ", url_date)
            if url_date:
                return Url(shortened_url=url_date["shortened_url"],
                           original_url=url_date["original_url"],
                           created_at=url_date["created_at"],
                           expires_at=url_date["expires_at"],
                           url_id=url_date["_id"]
                )
            return None
        except PyMongoError as e:
            print(f"Error finding URL: {e}")
            return None

    def find_by_original_url(self, original_url: str) -> Url:
        try:
            url_date = self.collection.find_one({"original_url": original_url})
            if url_date:
                return Url(shortened_url=url_date['shortened_url'], original_url=url_date["original_url"], created_at=url_date["created_at"],)
            return None
        except PyMongoError as e:
            print(f"Error finding URL: {e}")
            return None

    def delete_by_shortened_url(self, shortened_url: str) -> Url:
        try:
            result = self.collection.delete_one({"shortened_url": shortened_url})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting URL: {e}")
            return False

    def delete_expired_url(self) -> int:
        try:
            expired_date = datetime.now()
            result = self.collection.delete_many({"expires_at": {"$lt": expired_date}})
        except PyMongoError as e:
            print(f"Error deleting URL: {e}")
            return 0