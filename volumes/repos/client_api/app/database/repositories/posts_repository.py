import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.configs.dbs import get_mysql_db, get_postgres_db
from app.database.models.CustomerData.PostsModel import PostsModel
from app.database.repositories.BaseAppRepository import RepoResponse
from app.exceptions.data.PostsExceptions import InsertException
from app.log.loggers.app_logger import log_exception

# Logging
log = logging.getLogger(__name__)


class PostsRepository:
    mysqldb: Session = Depends(get_mysql_db)
    postgresdb: Session = Depends(get_postgres_db)

    def __init__(self) -> None:
        super().__init__()
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
        Also save, store
        :return: RepoResponse
        """

        log.debug('%s - Received data for a new post.', self.__class__.__name__)
        # log.debug("title = %s", title)
        # log.debug("content = %s", content)
        # log.debug("rating = %s", rating)
        # log.debug("published = %s", published)

        try:
            new_model = PostsModel(
                title=title,
                content=content,
                rating=rating,
                published=published
            )
            log.debug('%s - Created a posts model with the new post data.', self.__class__.__name__)
            # log.debug("new_model title = %s", new_model.title)
            # log.debug("new_model content = %s", new_model.content)
            # log.debug("new_model rating = %s", new_model.rating)
            # log.debug("new_model published = %s", new_model.published)

            self.postgresdb.add(new_model)
            self.postgresdb.commit()
            self.postgresdb.refresh(new_model)
            log.debug('%s - Added and commited to the postgres db.', self.__class__.__name__)

            return RepoResponse(
                status=True,
                data=new_model,
                errors={},
                meta={},
            )

        except Exception as e:
            log_exception(log, e)
            raise InsertException("The posts repository could not insert a post")


    def find_all(self):
        """
        alias for get_all
        alias for list
        :return: RepoResponse
        """
        try:
            posts = self.postgresdb.query(PostsModel).filter(PostsModel.deleted_at == None).all()

            return RepoResponse(
                status=True,
                data=posts,
                errors={},
                meta={},
            )
        except Exception as e:
            log.debug(e)
            log_exception(log, e)
            raise Exception("The posts repository could not find all posts")


    def find_one_by_uuid(self, post_uuid):
        try:
            post = (self.postgresdb.query(PostsModel)
                     .filter(
                        PostsModel.uuid == post_uuid,
                        PostsModel.deleted_at.is_(None)
                    )
                    .first())

            return RepoResponse(
                status=True,
                data=post,
                errors={},
                meta={},
            )
        except Exception as e:
            log.debug(e)
            log_exception(log, e)
            raise Exception(f"The posts repository could not find the post identified by uuid {post_uuid}")

    def delete_post_by_uuid(self, post_uuid):
        log.debug("Repository is deleting a post by the uuid %s", post_uuid)
        log.debug(post_uuid)
        log.debug(type(post_uuid))

        try:
            post = (self.postgresdb
                .query(PostsModel)
                .filter(PostsModel.uuid == post_uuid)
                .delete(synchronize_session=False))
            self.postgresdb.commit()

            return RepoResponse(
                status=True,
                data=post,
                errors={},
                meta={},
            )

        except Exception as e:
            log.debug(e)
            log_exception(log, e)
            raise Exception(f"The posts repository could not delete the post identified by uuid {post_uuid}")

    def mark_one_as_deleted_by_uuid(self, post_uuid):
        try:
            post = (self.postgresdb.query(PostsModel)
                     .filter(PostsModel.uuid == post_uuid)
                     .delete(synchronize_session=False))

            return post
        except Exception as e:
            log.debug(e)
            log_exception(log, e)
            raise Exception(f"The posts repository could not delete the post identified by uuid {post_uuid}")




