import logging
from typing import Final

from fastapi import Depends
from pydantic import ValidationError
from redis.exceptions import ConnectionError
from redis_om import NotFoundError

from app.database.configs.dbs import get_redis_cache
from app.database.models.ClientCache.PostsModel import PostsCacheModel
from app.database.repositories.BaseAppRepository import RepoResponse
from app.log.loggers.app_logger import log_exception

log = logging.getLogger(__name__)


class PostsCacheRepository:
    KEY_GET_ALL: Final[str] = 'get_all_posts'
    MODEL_EXPIRATION_SECONDS: Final[int] = 60 * 60 * 24

    redis_cache: Depends(get_redis_cache)

    def __init__(self):
        self.redis_cache = get_redis_cache()


    @staticmethod
    def repo_response(status: bool, message: str, data: dict, errors: dict, meta=None):
        """
        The repo response creates a consistent data structure response that the
        consumer of this repository can expect.
        todo: convert to pydantic model
        :param status:
        :param message:
        :param data:
        :param errors:
        :param meta:
        :return: dict
        """
        return {
            "status": status,
            "message": message,
            "data": data,
            "errors": errors,
            "meta": meta if meta is not None else {},
        }


    def store_post(self, post: dict):
        # assert PostsCacheModel.get(new_cache_post.pk) == new_cache_post
        log.debug('%s - Storing a post.', self.__class__.__name__)

        try:
            new_cache_post = PostsCacheModel(
                id=post["id"],
                uuid=str(post["uuid"]),
                title=post["title"],
                content=post["content"],
                published="TRUE" if post["published"] else "FALSE",
                rating=post["rating"],
                created_at=post["created_at"].isoformat(),
                updated_at=post["updated_at"].isoformat(),
                deleted_at="NULL" if post["deleted_at"] is None else post["deleted_at"].isoformat(),
            )
            new_cache_post.save()
            new_cache_post.expire(self.MODEL_EXPIRATION_SECONDS)
            log.debug('%s - The post was successfully cached.', self.__class__.__name__)
            log.debug(new_cache_post)

            return RepoResponse(
                status=True,
                data={
                    "model": new_cache_post,
                },
                meta={},
                errors={},
            )
        except ValidationError as e:
            log.debug(e)
        except Exception as e:
            log_exception(log, e)
            raise Exception("The posts cache repository could not cache a post")


    def find_one_wt_cache_key(self, cache_key: str):
        log.debug("%s - Retrieving a post using the cache key %s.", self.__class__.__name__, cache_key)

        try:
            return RepoResponse(
                status=True,
                data={
                    "model": PostsCacheModel.get(cache_key),
                },
                meta={},
                errors={},
            )
        except NotFoundError as e:
            log_exception(log, e)








    def find_all(self):
        """
        Get all posts
         - alias for get_all
         - alias for list
        :return: RepoResponse
        """
        log.debug('%s - Retrieving all posts.', self.__class__.__name__)

        try:
            cached_posts = []
            for pk in PostsCacheModel.all_pks():
                cached_posts.append(PostsCacheModel.get(pk))
            log.debug("The posts cache repo has retrieved all cached posts.")
            log.debug(cached_posts)

            return RepoResponse(
                status=True,
                data=cached_posts,
                meta={
                    "count": len(cached_posts)
                },
                errors={},
            )

        except ValidationError as e:
            log.debug(e)
        except ConnectionError as e:
            log.critical("Could not connect to the cache repository resource. e.args = %s", e.args)
            raise Exception(f"Could not connect to the cache repository resource. {e.args}")
        except Exception as e:
            log_exception(log, e)
            raise Exception("Could not get all posts for the current API user.")


    def do_cached_posts_exist(self) -> bool:
        log.debug("Checking if all posts have been previously cached.")
        cache_key = f"{self.KEY_GET_ALL}"
        return self.redis_cache.exists(cache_key)

    @staticmethod
    def delete_post_by_uuid(post_uuid):
        log.debug("The cache repository is deleting a post using the uuid %s", post_uuid)
        log.debug(post_uuid)
        log.debug(type(post_uuid))

        try:
            deleted_cache_model =  PostsCacheModel.find(PostsCacheModel.uuid == post_uuid.hex).delete()
            log.debug(deleted_cache_model)
            log.debug(type(deleted_cache_model))
            return deleted_cache_model
        except NotFoundError as e:
            log_exception(log, e)




