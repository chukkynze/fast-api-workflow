import json
from datetime import timezone
import datetime
from typing import Any
from app.database.models.CustomerData.PostsModel import PostsModel
from app.database.repositories.posts_cache_repository import PostsCacheRepository
from app.database.repositories.posts_repository import PostsRepository
from app.exceptions.data.PostsExceptions import CreatePostFailurePostServiceException, CachePostFailurePostServiceException
from app.log.loggers.app_logger import log_exception, get_service_logger
from app.schemas.PostRequestsSchemas import CreatePostInsertDataSchema, GetPostResponseDataSchema

# Logging
log = get_service_logger()

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






    # Get a Post
    def create_post(self, new_post_data: CreatePostInsertDataSchema):
        log.debug('Service is processing new post data.')

        try:
            log.debug("Service is trying to send new post data to the repository.")
            new_model = self.posts_repo.insert(**new_post_data.model_dump())
            log.debug("The new model is:")
            log.debug(new_model)
            cache_res = self.store_post_in_cache(new_model)

            status = True
            data = {
                "id": new_model.id,
                "uuid": new_model.uuid,
                "title": new_model.title,
                "content": new_model.content,
                "rating": new_model.rating,
                "published": new_model.published,
                "created_at": new_model.created_at,
                "updated_at": new_model.updated_at,
                "deleted_at": new_model.deleted_at,
            }
            meta = {"cached_model": cache_res}
            errors = {}

            return self.service_response(
                status,
                data,
                errors,
                meta
            )
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


    # Get All Posts
    def get_posts(self):
        log.debug('Service is getting all posts.')

        cached_posts = self.posts_cache.find_all()
        log.debug("The posts service has received all cached posts from the cache repository.")
        log.debug(cached_posts)
        log.debug(type(cached_posts))

        if len(cached_posts.len) == 0:
            log.debug("No posts exist in cache. Retrieving from the repo instead.")
            repo_posts = self.get_posts_from_repo()
            log.debug("Retrieved all posts from the repo.")
            log.debug(repo_posts)
            log.debug(type(repo_posts))

            try:
                self.store_posts_in_cache(repo_posts)
            except Exception as e:
                log_exception(log, e)
        else:
            posts = []
            for cached_post in cached_posts:
                cleaned_post = GetPostResponseDataSchema(
                    id=cached_post.id,
                    uuid=cached_post.uuid,
                    title=cached_post.title,
                    content=cached_post.content,
                    published=cached_post.published,
                    rating=cached_post.rating,
                    created_at=cached_post.created_at,
                    updated_at=cached_post.updated_at,
                    deleted_at=cached_post.deleted_at,
                )
                posts.append(cleaned_post)


        status = True
        data = posts
        errors = {}

        return self.service_response(
            status=status,
            data=data,
            errors=errors,
            meta={
                "total_posts": len(posts)
            }
        )


    def get_posts_from_repo(self):
        log.debug("Retrieving posts from the repo.")
        try:
            return self.posts_repo.find_all()
        except Exception as e:
            log_exception(log, e)
            raise Exception("The service could not get all stored posts from the repo.")

    def store_posts_in_cache(self, posts):
        log.debug("Storing posts in the cache repository.")
        try:
            if len(posts) > 0:
                post_cache_data = self.convert_model_to_cacheable_data(posts)
                self.posts_cache.store_posts(post_cache_data)
            else:
                log.debug("There are %s posts. Will not cache an empty list.", posts.len())
        except Exception as e:
            log_exception(log, e)
            raise Exception("The service could not store posts in the cache repository.")

    def do_cached_posts_exist(self) -> bool:
        log.debug("Checking the cache repository for cached set of all posts.")
        cache = self.posts_cache
        return cache.do_cached_posts_exist()










    def delete_post(self, post_id):
        # delete cache

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
