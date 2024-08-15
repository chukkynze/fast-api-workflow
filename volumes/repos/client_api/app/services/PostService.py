import random
from random import randrange
from datetime import timezone
import datetime
from typing import Any


class PostService:
    """
    This is the PostService class which handles all CRUD operations
    and related functionality for Posts.
    """
    range_max = 100000
    post_db = [
        {
            "id": 1,
            "title": "title for post 1.",
            "content": "content for post 1.",
            "published": True,
            "rating": random.uniform(0.0, 5.0),
        },
        {
            "id": 2,
            "title": "title for post 2.",
            "content": "content for post 2.",
            "published": False,
            "rating": random.uniform(0.0, 5.0),
        },
    ]

    def create_post(self, new_post_data: dict):

        status = True
        # new_model = insert(new_post_data)
        data = {
            "id": randrange(1, self.range_max),
            "title": new_post_data["title"],
            "content": new_post_data['content'],
            "rating": new_post_data['rating'],
            "published": new_post_data['published'],
            "created_at": self.get_utc_timestamp(),
        }
        self.post_db.append(data)
        errors: dict[Any, Any] = {}

        return self.service_response(
            status,
            data,
            errors
        )

    @staticmethod
    def service_response(status: bool, data: dict, errors: dict):
        """
        The service response creates a consistent data structure response that the
        consumer of this service can expect. There is no message because the consumer
        of this service will be responsible for creating and formatting the 'message' to
        the end consumer/user of the API

        :param status:
        :param data:
        :param errors:
        :return:
        """
        return {
            "status": status,
            "data": data,
            "errors": errors
        }

    @classmethod
    def get_posts(cls):
        return cls.post_db

    @staticmethod
    def get_utc_timestamp():
        # Getting the current date
        # and time
        dt = datetime.datetime.now(timezone.utc)

        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()

        return utc_timestamp

    def delete_post(self, post_id):

        status = True
        data = {}
        errors: dict[Any, Any] = {}  # type: ignore

        return self.service_response(
            status,
            data,
            errors
        )

    def get_post(self, post_id):

        print(self.post_db[post_id])
        print(type(self.post_db[post_id]))

        return self.post_db[post_id]

    def update_post(self, post_id, new_post_data):

        print(self.post_db[post_id])
        print(type(self.post_db[post_id]))

        print(new_post_data)
        print(type(new_post_data))

        status = True
        data = {}
        errors: dict[Any, Any] = {}  # type: ignore

        return self.service_response(
            status,
            data,
            errors
        )

    def patch_post(self, post_id, new_post_data):

        print(self.post_db[post_id])
        print(type(self.post_db[post_id]))

        print(new_post_data)
        print(type(new_post_data))

        status = True
        data = {}
        errors: dict[Any, Any] = {}  # type: ignore

        return self.service_response(
            status,
            data,
            errors
        )
