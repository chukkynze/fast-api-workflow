import logging

from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.configs.dbs import get_mysql_db, get_postgres_db
from app.database.models.CustomerData.PostsModel import PostsModel
from app.exceptions.data.PostsExceptions import PostsRepositoryInsertException
from app.log.loggers.app_logger import log_exception


# Logging
log = logging.getLogger(__name__)


class PostsRepository:
    mysqldb: Session = Depends(get_mysql_db)
    postgresdb: Session = Depends(get_postgres_db)

    def __init__(self) -> None:
        self.mysqldb = get_mysql_db()
        self.postgresdb = get_postgres_db()


    def insert(
            self,
            title: str,
            content: str,
            rating: float,
            published: bool,
    ):
        """
        this will break the find_all cache
        but in the service?
        :return:
        """

        log.debug("Repository has received data for a new post.")
        # log.debug("title = %s", title)
        # log.debug("content = %s", content)
        # log.debug("rating = %s", rating)
        # log.debug("published = %s", published)

        new_post = PostsModel(
            title=title,
            content=content,
            rating=rating,
            published=published
        )
        log.debug("Created a posts model with the new post data.")
        # log.debug("new_post title = %s", new_post.title)
        # log.debug("new_post content = %s", new_post.content)
        # log.debug("new_post rating = %s", new_post.rating)
        # log.debug("new_post published = %s", new_post.published)

        try:
            log.debug("Trying to add and commit to the postgres db.")
            self.postgresdb.add(new_post)
            self.postgresdb.commit()
            self.postgresdb.refresh(new_post)

            return new_post

        except Exception as e:
            log_exception(log, e)
            raise PostsRepositoryInsertException("The posts repository could not create a new post")


    def find_all(self):
        """
        alias for get_all
        alias for list
        :return:
        """
        try:
            posts = self.postgresdb.query(PostsModel).all()
            return posts
        except Exception as e:
            log.debug(e)
            log_exception(log, e)
            raise Exception("The posts repository could not find all posts")

    def find_one(self, post_uuid):
        try:
            post = (self.postgresdb.query(PostsModel)
                     .filter(PostsModel.uuid == post_uuid)
                     .first())

            return post
        except Exception as e:
            log.debug(e)
            log_exception(log, e)
            raise Exception("The posts repository could not find all posts")


