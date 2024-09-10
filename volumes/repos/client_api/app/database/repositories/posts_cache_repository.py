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
            new_cache_post.expire(self.MODEL_EXPIRATION_SECONDS)
            new_cache_post.save()
            log.debug('%s - The post was successfully cached.', self.__class__.__name__)
            log.debug(new_cache_post)

            return RepoResponse(
                status=True,
                data=new_cache_post,
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
            cached_post = PostsCacheModel.get(cache_key)
            log.debug(cached_post)
            log.debug(type(cached_post))

            return RepoResponse(
                status=True,
                data=cached_post,
                meta={},
                errors={},
            )
        except NotFoundError as e:
            log_exception(log, e)
            raise Exception("Someting don happen ohh!")
        except Exception as e:
            log_exception(log, e)
            raise Exception("Unknown tin don happen!!")


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


    def delete_post_by_uuid(self, post_uuid):
        log.debug("%s - Deleting a post with the uuid %s.", self.__class__.__name__, post_uuid)
        log.debug(post_uuid)
        log.debug(type(post_uuid))

        try:
            deleted_cache_model =  (
                PostsCacheModel
                .find(PostsCacheModel.uuid == str(post_uuid))
                .delete()
            )

            return RepoResponse(
                status=True,
                data=deleted_cache_model,
                meta={},
                errors={},
            )

        except NotFoundError as e:
            log_exception(log, e)
            raise Exception("Someting don happen ohh!")


    def find_one_wt_uuid(self, post_uuid):
        log.debug("%s - Retrieving a post using the uuid %s.", self.__class__.__name__, post_uuid)

        try:
            cache_model = (
                PostsCacheModel
                .find(PostsCacheModel.uuid == str(post_uuid))
                .first()
            )

            return RepoResponse(
                status=True,
                data=cache_model,
                meta={},
                errors={},
            )
        except NotFoundError as e:
            log_exception(log, e)
            raise Exception("Someting don happen ohh!")


    def patch_one_by_uuid(self, post_uuid, patched_merged_model):
        log.debug("%s - Patching a cached post with the uuid %s.", self.__class__.__name__, post_uuid)
        log.debug(post_uuid)
        log.debug(type(post_uuid))
        log.debug(patched_merged_model)
        log.debug(type(patched_merged_model))

        try:
            updated_cache_model =  (
                PostsCacheModel
                .find(PostsCacheModel.uuid == str(post_uuid))
                .update(
                    title=patched_merged_model['title'],
                    content=patched_merged_model['content'],
                    published="TRUE" if patched_merged_model["published"] else "FALSE",
                    rating=patched_merged_model['rating'],
                    updated_at=patched_merged_model['updated_at'].isoformat(),
                )
            )

            log.debug("updated_cache_model = ")
            log.debug(updated_cache_model)
            log.debug(type(updated_cache_model))

            return RepoResponse(
                status=True,
                data=True,
                meta={},
                errors={},
            )

        except ValidationError as e:
            log.debug(e)
        except Exception as e:
            log_exception(log, e)
            raise Exception("Someting don happen ohh!")



