import datetime
import json
import logging
import uuid
from datetime import timezone
from typing import Any
from pydantic import ValidationError
from app.database.models.CustomerData.PostsModel import PostsModel
from app.database.repositories.posts_cache_repository import PostsCacheRepository
from app.database.repositories.posts_repository import PostsRepository
from app.exceptions.data.PostsExceptions import (
    CreationException, DeleteException, StorageException,
    CacheException, ReadOneException, CacheKeyPostUuidMismatchException,
    ReadOneCachedException
)
from app.log.loggers.app_logger import log_exception
from app.schemas.PostRequestsSchemas import CreatePostInsertDataSchema, GetPostResponseDataSchema, CreatePostResponseDataSchema
from app.services.BaseAppService import ServiceResponse


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
        super().__init__()
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
        log.debug(f'The %s has initiated creating a post.', self.__class__.__name__)

        try:
            stored_model = self.store_post_in_db(new_post_data)

            if stored_model is None:
                raise Exception("Could not store the post in the db.")

            log.debug('%s - The new model is:', self.__class__.__name__)
            log.debug(stored_model.__dict__)

            cached_model = self.store_post_in_cache(stored_model)

            output_data = CreatePostResponseDataSchema(
                uuid=str(stored_model.uuid),
                title=stored_model.title,
                content=stored_model.content,
                rating=stored_model.rating,
                published=stored_model.published,
                created_at=stored_model.created_at,
                updated_at=stored_model.updated_at,
                deleted_at=None if stored_model.deleted_at == "" else stored_model.deleted_at,
            ).model_dump()

            status = True
            data = output_data
            meta = {
                "completed": {
                    "at": datetime.datetime.now().isoformat(),
                },
                "model": {
                    "cache_key": cached_model.pk
                }
            }
            errors = {}

            return ServiceResponse(
                status=status,
                data=data,
                errors=errors,
                meta=meta,
            )
        except ValidationError as e:
            log.debug(e)
            raise CreationException('Data from the repo is not acceptable to the posts service layer.')
        except Exception as e:
            log_exception(log, e)
            raise CreationException('Could not create a post in the posts service layer.')

    def store_post_in_db(self, new_post_data: CreatePostInsertDataSchema):
        """
        Store a single post in the database.
        :param new_post_data: CreatePostInsertDataSchema
        :return:
        """
        log.debug('%s - Storing a post in the database.', self.__class__.__name__)

        try:
            repo_res = self.posts_repo.insert(**new_post_data.model_dump())
            log.debug('%s - Repo Response: ', self.__class__.__name__)
            log.debug(repo_res.dict())

            if not repo_res.status:
                output_model = None
            else:
                log.debug('%s - Stored post: ', self.__class__.__name__)
                log.debug(repo_res.data)
                output_model = repo_res.data

            return output_model

        except Exception as e:
            log_exception(log, e)
            raise StorageException("The service could not store a post in the posts repository.")

    def store_post_in_cache(self, post: PostsModel):
        """
        Store a single post in the cache.
        Returns a PostsCacheModel including the pk which can be used to get the model later.
        There are other indexes on the PostsCacheModel available for searching
        :param post:
        :return: PostsCacheModel | None
        """
        log.debug('%s - Storing a post in the cache.', self.__class__.__name__)

        try:
            cache_res = self.posts_cache.store_post(post.__dict__)
            log.debug('%s - Repo Response: ', self.__class__.__name__)
            log.debug(cache_res.dict())

            if not cache_res.status:
                output_model = None
            else:
                log.debug('%s - Cached post: ', self.__class__.__name__)
                log.debug(cache_res.data)
                output_model = cache_res.data

            return output_model

        except Exception as e:
            log_exception(log, e)
            raise CacheException("The service could not store posts in the cache repository.")

    # Read
    def get_post(self, post_uuid: uuid, cache_key: str = None):
        log.debug('The %s is retrieving data for the post with uuid = %s.', self.__class__.__name__, post_uuid)

        try:
            # Check if the cache key provided will find a cached mode
            # of course check if the returned model has the same uuid as the sent post uuid
            cached_model = self.get_post_from_cache_wt_key(cache_key, post_uuid)

            # if the cached model is still None, we get the model from the db
            # of course we store the newly retrieved model in the cache as well
            if cached_model is None:
                repo_res = self.posts_repo.find_one_by_uuid(post_uuid)
                log.debug('%s - Repo Response: ', self.__class__.__name__)
                log.debug(repo_res.dict())

                if repo_res.data is None:
                    status = False
                    data = {
                        "err_msg": f"No model with the uuid {post_uuid} was found."
                    }
                    meta = {
                        "completed": {
                            "at": datetime.datetime.now().isoformat(),
                        },
                        "model": None
                    }
                    errors = {}

                    return ServiceResponse(
                        status=status,
                        data=data,
                        errors=errors,
                        meta=meta
                    )
                else:
                    output_model = repo_res.data
                    cached_model = self.store_post_in_cache(output_model)

            else:
                output_model = cached_model
                log.debug("The retrieved cached model is:")
                log.debug(output_model.__dict__)

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
                    "cache_key": cached_model.pk
                }
            }
            errors = {}

            return ServiceResponse(
                status=status,
                data=data,
                errors=errors,
                meta=meta
            )

        except Exception as e:
            log_exception(log, e)
            raise ReadOneException(f'The {self.__class__.__name__} could not retrieve the post with uuid = {post_uuid} and cache key = {cache_key}.')

    def get_post_from_cache_wt_key(self, cache_key: str | None, post_uuid: uuid):
        """
        Get a single post from the cache. Ensure the uuid of the retrieved post using the cache key
        matches the uuid sent as an argument from the request
        :param post_uuid:
        :param cache_key:
        :return: PostsCacheModel | None
        """
        log.debug('%s - Retrieving a post from the cache.', self.__class__.__name__)

        try:

            if cache_key is None:
                log.debug("Cache key is None.")
                cache_res = None
            else:
                log.debug('Service is searching in the cache for the post using its cache key %s.', cache_key)
                repo_res = self.posts_cache.find_one_wt_cache_key(cache_key)
                log.debug('%s - Repo Response: ', self.__class__.__name__)
                log.debug(repo_res.dict())

                log.debug("UUID from the request: %s", post_uuid)
                log.debug("UUID from the cached model: %s", repo_res.data['model'].uuid)

                if repo_res.data['model'].uuid != str(post_uuid):
                    raise CacheKeyPostUuidMismatchException(f"The post uuid retrieved from the model found with the cache key does not match the post uuid sent in the request.")
                else:
                    cache_res = repo_res.data['model']
                    log.debug("Cache Results are: ")
                    log.debug(cache_res)
                    log.debug(type(cache_res))

            return cache_res

        except Exception as e:
            log_exception(log, e)
            raise ReadOneCachedException("The service could not get a post from the cache repository.")

    def get_posts(self):
        log.debug('The %s is retrieving all posts.', self.__class__.__name__)

        repo_res = self.posts_cache.find_all()
        log.debug('%s - Repo Response: ', self.__class__.__name__)
        log.debug(repo_res.dict())

        if repo_res.meta['count'] == 0:
            log.debug('%s - No posts exist in cache. Retrieving from the repo instead.', self.__class__.__name__)
            posts = self.get_posts_from_repo()
            log.debug("Retrieved all posts from the repo.")
            log.debug(posts)
            log.debug(type(posts))

        else:
            posts = []
            for cached_post in repo_res.data:
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
        return ServiceResponse(
            status=status,
            data=data,
            errors=errors,
            meta=meta
        )

    def get_posts_from_repo(self):
        log.debug("Retrieving posts from the repo.")
        try:
            return self.posts_repo.find_all().data
        except Exception as e:
            log_exception(log, e)
            raise Exception("The service could not get all stored posts from the repo.")



    # Delete
    def delete_post(self, post_uuid: uuid):
        log.debug('The %s is deleting the post with uuid = %s.', self.__class__.__name__, post_uuid)

        try:
            repo_res = self.posts_repo.delete_post_by_uuid(post_uuid)
            log.debug('%s - Repo Response: ', self.__class__.__name__)
            log.debug(repo_res.dict())

            output_model = repo_res.data
            log.debug("output_model = ")
            log.debug(output_model)

            self.posts_cache.delete_post_by_uuid(post_uuid)

            return ServiceResponse(
                status=True,
                data={},
                errors={},
                meta={}
            )
        except Exception as e:
            log_exception(log, e)
            raise DeleteException("The service could not delete a post from the posts repository.")




    # Update
    def mark_post_as_deleted(self, post_uuid: uuid):
        log.debug('Service is marking data as deleted for the post with uuid = %s.', post_uuid)

        try:
            output_model = self.posts_repo.mark_one_as_deleted_by_uuid(post_uuid)
            log.debug("output_model = ")
            log.debug(output_model)

            return self.service_response(True, {}, {})
        except Exception as e:
            log_exception(log, e)
            raise DeletePostFailurePostServiceException("The service could not delete a post from the posts repository.")

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
