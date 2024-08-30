import logging
from functools import lru_cache

from redis_om import get_redis_connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_app_env_config

log = logging.getLogger(__name__)
app_env_config = get_app_env_config()

@lru_cache(maxsize=None)
def get_redis_cache():
    """
    Retrieving the redis cache connection.
    :return:
    """
    # Note: the Redis maxmemory directive is used to limit the memory usage to a fixed amount.
    # See: https://redis.io/docs/latest/develop/reference/eviction/
    # REDIS_OM_URL overrides this
    return get_redis_connection(
        # url=f"{app_env_config.REDIS_CACHE_DRIVERNAME}://{app_env_config.REDIS_CACHE_USERNAME}:{app_env_config.REDIS_CACHE_PASSWORD.get_secret_value()}@{app_env_config.REDIS_CACHE_HOST}:{app_env_config.REDIS_CACHE_PORT}",
        db=app_env_config.REDIS_CACHE_PRIMARY_DB,
        encoding="utf8",
    )

@lru_cache(maxsize=None)
def get_mysql_db():
    """
    Retrieving the mysql db connection.
    :return: A SqlAlchemy Session - sqlalchemy.orm.session.sessionmaker
    """
    mysql_engine = create_engine(
        f"{app_env_config.MYSQLDB_DRIVERNAME}://{app_env_config.MYSQLDB_USERNAME}:{app_env_config.MYSQLDB_PASSWORD.get_secret_value()}@{app_env_config.MYSQLDB_HOST}:{app_env_config.MYSQLDB_PORT}/{app_env_config.MYSQLDB_DATABASE}",
        echo=app_env_config.MYSQLDB_ECHO_LOG_LEVEL,
        future=app_env_config.MYSQLDB_FUTURE
    )
    mysql_session = sessionmaker(
        bind=mysql_engine,
        autocommit=app_env_config.MYSQLDB_SESSION_AUTOCOMMIT,
        autoflush=app_env_config.MYSQLDB_SESSION_AUTOFLUSH,
    )

    return mysql_session()

@lru_cache(maxsize=None)
def get_postgres_db():
    """
    Retrieving the postgres db connection.
    :return: A SqlAlchemy Session - sqlalchemy.orm.session.sessionmaker
    """
    log.debug("Retrieving the postgres db connection.")
    postgres_engine = create_engine(
        f"{app_env_config.POSTGRESDB_DRIVERNAME}://{app_env_config.POSTGRESDB_USERNAME}:{app_env_config.POSTGRESDB_PASSWORD.get_secret_value()}@{app_env_config.POSTGRESDB_HOST}:{app_env_config.POSTGRESDB_PORT}/{app_env_config.POSTGRESDB_DATABASE}",
        echo=app_env_config.POSTGRESDB_ECHO_LOG_LEVEL,
        future=app_env_config.POSTGRESDB_FUTURE
    )
    postgres_session = sessionmaker(
        bind=postgres_engine,
        autocommit=app_env_config.POSTGRESDB_SESSION_AUTOCOMMIT,
        autoflush=app_env_config.POSTGRESDB_SESSION_AUTOFLUSH,
    )

    return postgres_session()
