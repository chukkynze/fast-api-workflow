import json
import logging
from datetime import timezone
import datetime
from typing import Any

import uuid
from pydantic import ValidationError

from app.database.models.CustomerData.PostsModel import PostsModel
from app.database.repositories.posts_cache_repository import PostsCacheRepository
from app.database.repositories.posts_repository import PostsRepository
from app.exceptions.data.PostsExceptions import CreatePostFailurePostServiceException, \
    CachePostFailurePostServiceException, GetCachedPostFailurePostServiceException
from app.log.loggers.app_logger import log_exception
from app.schemas.PostRequestsSchemas import CreatePostInsertDataSchema, GetPostResponseDataSchema, \
    CreatePostResponseDataSchema

# Logging
log = logging.getLogger(__name__)

class PostService:
    """
    This is the PostService class which handles all CRUD operations
    and related functionality for Posts.
    """
    posts_repo: PostsRepository
    posts_cache_repo: PostsCacheRepository

    def __init__(self) -> None:
        self.posts_repo = PostsRepository()
        self.posts_cache = PostsCacheRepository()


    @staticmethod
    def service_response(status: bool, data: dict, errors: dict, meta=None):
        """
        The service response creates a consistent data structure response that the
        consumer of this service can expect. There is no message because the consumer
        of this service will be responsible for creating and formatting the 'message' to
        the end consumer/user of the API

        :param status:
        :param data:
        :param errors:
        :param meta:
        :return:
        """
        return {
            "status": status,
            "data": data,
            "errors": errors,
            "meta": meta if meta is not None else {},
        }

    @staticmethod
    def format_posts(posts):
        return json.dumps(posts)

    @staticmethod
    def get_utc_timestamp():
        # Getting the current date
        # and time
        dt = datetime.datetime.now(timezone.utc)

        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()

        return utc_timestamp

    @staticmethod
    def convert_model_to_cacheable_data(posts):
        log.debug("Converting models to dicts for insertion to cache.")
        log.debug(posts)
        log.debug(type(posts))
        cacheable_data = {}

        if len(posts) > 0:
            for post in posts:
                cacheable_data[post.uuid.hex] = {
                    "id": post.id,
                    "uuid": post.uuid.hex,
                    "title": post.title,
                    "content": post.content,
                    "rating": post.rating,
                    "published": post.published,
                    "created_at": post.created_at.isoformat(),
                    "updated_at": post.updated_at.isoformat(),
                    "deleted_at": post.deleted_at.isoformat() if post.deleted_at else "null",
                }

        return cacheable_data






    # Create
    def create_post(self, new_post_data: CreatePostInsertDataSchema):
        log.debug('Service is processing new post data.')

        try:
            log.debug("The Posts Service is attempting to send new post data to the repository.")
            new_model = self.posts_repo.insert(**new_post_data.model_dump())
            log.debug("The new model is:")
            log.debug(new_model.__dict__)

            cache_res = self.store_post_in_cache(new_model)

            output_data = CreatePostResponseDataSchema(
                uuid=str(new_model.uuid),
                title=new_model.title,
                content=new_model.content,
                rating=new_model.rating,
                published=new_model.published,
                created_at=new_model.created_at,
                updated_at=new_model.updated_at,
                deleted_at=None if new_model.deleted_at == "" else new_model.deleted_at,
            ).model_dump()

            status = True
            data = output_data
            meta = {
                "completed": {
                    "at": datetime.datetime.now().isoformat(),
                },
                "model": {
                    "cache_key": cache_res.pk
                }
            }
            errors = {}

            return self.service_response(
                status,
                data,
                errors,
                meta
            )
        except ValidationError as e:
            log.debug(e)
            raise CreatePostFailurePostServiceException('Data from the repo is not acceptable to the posts service layer.')
        except Exception as e:
            log_exception(log, e)
            raise CreatePostFailurePostServiceException('Could not create a post in the posts service layer.')

    def store_post_in_cache(self, post: PostsModel):
        """
        Store a single post in the cache for easy retrieval later.
        Returns a PostsCacheModel including the pk which can be used to get the model later.
        There are other indexes on the PostsCacheModel available for searching
        :param post:
        :return: PostsCacheModel
        """
        log.debug("Storing a post in the cache repository.")

        try:
            cache_res = self.posts_cache.store_post(post.__dict__)
            log.debug("Cache Results are: ")
            log.debug(cache_res)

            return cache_res

        except Exception as e:
            log_exception(log, e)
            raise CachePostFailurePostServiceException("The service could not store posts in the cache repository.")


    # Read
    def get_post(self, post_uuid: uuid, cache_key: str = None):
        log.debug('Service is retrieving data for the post with uuid = %s.', post_uuid)

        cache_res = self.get_post_from_cache_wt_key(cache_key)
        log.debug(cache_res)
        log.debug(type(cache_res))

        if cache_res is None:
            output_model = self.posts_repo.find_one(post_uuid)
            log.debug("The retrieved model is:")
            log.debug(output_model.__dict__)
            log.debug("model.deleted_at = %s", output_model.deleted_at)
            log.debug(type(output_model.deleted_at))

            cache_res = self.store_post_in_cache(output_model)
        else:
            output_model = cache_res

        output_data = GetPostResponseDataSchema(
            uuid=str(output_model.uuid),
            title=output_model.title,
            content=output_model.content,
            rating=output_model.rating,
            published=output_model.published,
            created_at=output_model.created_at,
            updated_at=output_model.updated_at,
            deleted_at=None if output_model.deleted_at is None or 'NULL' else output_model.deleted_at,
        ).model_dump()

        status = True
        data = output_data
        meta = {
            "completed": {
                "at": datetime.datetime.now().isoformat(),
            },
            "model": {
                "cache_key": cache_res.pk
            }
        }
        errors = {}

        return self.service_response(
            status,
            data,
            errors,
            meta
        )

    def get_post_from_cache_wt_key(self, cache_key: str):
        log.debug("Getting a post from the cache repository using it's cache key.")

        try:
            cache_res = self.posts_cache.find_one_wt_cache_key(cache_key)
            log.debug("Cache Results are: ")
            log.debug(cache_res)

            return cache_res

        except Exception as e:
            log_exception(log, e)
            raise GetCachedPostFailurePostServiceException("The service could not get a post from the cache repository.")

    def get_posts(self):
        log.debug('Service is getting all posts.')

        cached_posts = self.posts_cache.find_all()
        log.debug("The posts service has received all cached posts from the cache repository.")
        log.debug(cached_posts)
        log.debug(type(cached_posts))

        if len(cached_posts) == 0:
            log.debug("No posts exist in cache. Retrieving from the repo instead.")
            posts = self.get_posts_from_repo()
            log.debug("Retrieved all posts from the repo.")
            log.debug(posts)
            log.debug(type(posts))

        else:
            posts = []
            for cached_post in cached_posts:
                cleaned_post = GetPostResponseDataSchema(
                    uuid=cached_post.uuid,
                    title=cached_post.title,
                    content=cached_post.content,
                    published=cached_post.published,
                    rating=cached_post.rating,
                    created_at=cached_post.created_at,
                    updated_at=cached_post.updated_at,
                    deleted_at=None if cached_post.deleted_at is None or 'NULL' else cached_post.deleted_at,
                )
                posts.append(cleaned_post)

        status = True
        data = posts
        errors = {}
        meta = {
            "completed": {
                "at": datetime.datetime.now().isoformat(),
            },
            "model": {
                "total_posts": len(posts)
            }
        }
        return self.service_response(
            status=status,
            data=data,
            errors=errors,
            meta=meta
        )

    def get_posts_from_repo(self):
        log.debug("Retrieving posts from the repo.")
        try:
            return self.posts_repo.find_all()
        except Exception as e:
            log_exception(log, e)
            raise Exception("The service could not get all stored posts from the repo.")















    # Delete
    def delete_post(self, post_uuid: uuid):
        log.debug('Service is deleting data for the post with uuid = %s.', post_uuid)

        status = True
        data = {}
        errors: dict[Any, Any] = {}  # type: ignore

        return self.service_response(
            status,
            data,
            errors
        )

    def update_post(self, post_id, new_post_data):
        # delete cache

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
        # delete cache

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
