import logging

from redis_om import get_redis_connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import config


log = logging.getLogger(__name__)


def get_redis_cache():
    """
    Retrieving the redis cache connection.
    :return:
    """
    # Note: the Redis maxmemory directive is used to limit the memory usage to a fixed amount.
    # See: https://redis.io/docs/latest/develop/reference/eviction/
    redis_client = get_redis_connection(
        url=f"{config.REDIS_CACHE_DRIVERNAME}://{config.REDIS_CACHE_USERNAME}:{config.REDIS_CACHE_PASSWORD.get_secret_value()}@{config.REDIS_CACHE_HOST}:{config.REDIS_CACHE_PORT}",
        db=config.REDIS_CACHE_PRIMARY_DB,
        encoding="utf8",
    )
    return redis_client

def get_redis_search():
    """
    Retrieving the redis search connection.
    :return:
    """
    # Note: the Redis maxmemory directive is used to limit the memory usage to a fixed amount.
    # See: https://redis.io/docs/latest/develop/reference/eviction/
    redis_client = get_redis_connection(
        url=f"{config.REDIS_SEARCH_DRIVERNAME}://{config.REDIS_SEARCH_USERNAME}:{config.REDIS_SEARCH_PASSWORD.get_secret_value()}@{config.REDIS_SEARCH_HOST}:{config.REDIS_SEARCH_PORT}",
        db=config.REDIS_SEARCH_PRIMARY_DB,
        encoding="utf8",
    )
    return redis_client

def get_mysql_db():
    """
    Retrieving the mysql db connection.
    :return: A SqlAlchemy Session - sqlalchemy.orm.session.sessionmaker
    """
    mysql_engine = create_engine(
        f"{config.MYSQLDB_DRIVERNAME}://{config.MYSQLDB_USERNAME}:{config.MYSQLDB_PASSWORD.get_secret_value()}@{config.MYSQLDB_HOST}:{config.MYSQLDB_PORT}/{config.MYSQLDB_DATABASE}",
        echo=config.MYSQLDB_ECHO_LOG_LEVEL,
        future=config.MYSQLDB_FUTURE
    )
    mysql_session = sessionmaker(
        bind=mysql_engine,
        autocommit=config.MYSQLDB_SESSION_AUTOCOMMIT,
        autoflush=config.MYSQLDB_SESSION_AUTOFLUSH,
    )

    return mysql_session()

def get_postgres_db():
    """
    Retrieving the postgres db connection.
    :return: A SqlAlchemy Session - sqlalchemy.orm.session.sessionmaker
    """
    log.debug("Retrieving the postgres db connection.")
    postgres_engine = create_engine(
        f"{config.POSTGRESDB_DRIVERNAME}://{config.POSTGRESDB_USERNAME}:{config.POSTGRESDB_PASSWORD.get_secret_value()}@{config.POSTGRESDB_HOST}:{config.POSTGRESDB_PORT}/{config.POSTGRESDB_DATABASE}",
        echo=config.POSTGRESDB_ECHO_LOG_LEVEL,
        future=config.POSTGRESDB_FUTURE
    )
    postgres_session = sessionmaker(
        bind=postgres_engine,
        autocommit=config.POSTGRESDB_SESSION_AUTOCOMMIT,
        autoflush=config.POSTGRESDB_SESSION_AUTOFLUSH,
    )

    return postgres_session()
