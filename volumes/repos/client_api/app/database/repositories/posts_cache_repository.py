import json
from typing import Final

from fastapi import Depends
from pydantic import ValidationError
from redis.exceptions import ConnectionError, AuthenticationError
from app.database.configs.dbs import get_redis_cache
from app.database.models.ClientCache.PostsModel import PostsCacheModel
from app.log.loggers.app_logger import get_repo_logger, log_exception


log = get_repo_logger()


class PostsCacheRepository:
    KEY_GET_ALL: Final[str] = 'get_all_posts'
    MODEL_EXPIRATION_SECONDS: Final[int] = 60 * 60 * 24

    redis_cache: Depends(get_redis_cache)

    def __init__(self):
        self.redis_cache = get_redis_cache()


    def store_post(self, post: dict):
        log.debug("The cache repository is storing a post.")
        # log.debug(json.dumps(post))

        try:
            new_cache_post = PostsCacheModel(
                id=post["id"],
                uuid=post["uuid"].hex,
                title=post["title"],
                content=post["content"],
                published="TRUE" if post["published"] else "FALSE",
                rating=post["rating"],
                created_at=post["created_at"].isoformat(),
                updated_at=post["updated_at"].isoformat(),
                deleted_at="NULL" if post["deleted_at"] is None else post["deleted_at"].isoformat(),
            )
            log.debug(new_cache_post)
            new_cache_post.save()
            new_cache_post.expire(self.MODEL_EXPIRATION_SECONDS)
            log.debug("key used to store the post with uuid %s is %s", new_cache_post.uuid, new_cache_post.key())

            return new_cache_post

        except ValidationError as e:
            log.debug(e)
        except AuthenticationError as e:
            log_exception(log, e)
        # assert PostsCacheModel.get(new_cache_post.pk) == new_cache_post








    def find_all(self):
        """
        alias for get_all
        alias for list
        :return:
        """
        log.debug("Cache repo is retrieving all posts.")

        try:
            log.debug("Trying to check if the cache key exists.")
            cached_posts_pks =  PostsCacheModel.all_pks()
            cached_posts = []
            for pk in cached_posts_pks:
                cached_posts.append(PostsCacheModel.get(pk))
            log.debug("The posts cache repo has retrieved all cached posts.")
            log.debug(cached_posts)
            return cached_posts
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


    def store_posts(self, posts):
        log.debug("The cache repository is storing posts")
        log.debug(posts)
        log.debug(type(posts))
        log.debug(json.dumps(posts))
        log.debug(type(json.dumps(posts)))
        self.redis_cache.hset(f"{self.KEY_GET_ALL}", json.dumps(posts))


    def insert(self):
        """
        this will break the find_all cache
        but in the service?
        :return:
        """
        pass

    def add_new_post_to_posts_cache(self, new_post):
        pass

    def delete_posts(self):
        pass
