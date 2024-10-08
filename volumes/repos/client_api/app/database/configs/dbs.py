import logging
from functools import lru_cache
from redis_om import get_redis_connection
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from config import get_app_env_config


log = logging.getLogger(__name__)
app_env_config = get_app_env_config()


# Redis
@lru_cache(maxsize=None)
def get_redis_cache():
    """
    Retrieving the redis cache connection.
    :return:
    """
    # Note: the Redis maxmemory directive is used to limit the memory usage to a fixed amount.
    # See: https://redis.io/docs/latest/develop/reference/eviction/
    # REDIS_OM_URL overrides the client no matter what
    # Note: Indexing only works for data stored in Redis logical database 0. If you are using a
    # different database number when connecting to Redis, you can expect the code to raise a
    # MigrationError when you run the migrator.
    return get_redis_connection(
        # url=f"{app_env_config.REDIS_CACHE_DRIVERNAME}://{app_env_config.REDIS_CACHE_USERNAME}:{app_env_config.REDIS_CACHE_PASSWORD.get_secret_value()}@{app_env_config.REDIS_CACHE_HOST}:{app_env_config.REDIS_CACHE_PORT}",
        db=app_env_config.REDIS_CACHE_PRIMARY_DB,
        encoding="utf8",
    )


# MySQL
@lru_cache(maxsize=None)
def get_mysql_db_engine()-> Engine:
    """
    Retrieving the MySQL db engine.
    :return: Engine - sqlalchemy.engine.Engine
    """
    log.debug("Retrieving the MySQL db engine.")
    return create_engine(
        f"{app_env_config.MYSQLDB_DRIVERNAME}://{app_env_config.MYSQLDB_USERNAME}:{app_env_config.MYSQLDB_PASSWORD.get_secret_value()}@{app_env_config.MYSQLDB_HOST}:{app_env_config.MYSQLDB_PORT}/{app_env_config.MYSQLDB_DATABASE}",
        echo=app_env_config.MYSQLDB_ECHO_LOG_LEVEL,
        future=app_env_config.MYSQLDB_FUTURE
    )

@lru_cache(maxsize=None)
def get_mysql_db():
    """
    Retrieving the mysql db connection.
    :return: A SqlAlchemy Session - sqlalchemy.orm.session.sessionmaker
    """
    log.debug("Retrieving the MySQL db session.")
    mysql_session = sessionmaker(
        bind=get_mysql_db_engine(),
        autocommit=app_env_config.MYSQLDB_SESSION_AUTOCOMMIT,
        autoflush=app_env_config.MYSQLDB_SESSION_AUTOFLUSH,
    )

    return mysql_session()


# Postgres
@lru_cache(maxsize=None)
def get_postgres_db_engine()-> Engine:
    """
    Retrieving the postgres db engine.
    :return: Engine - sqlalchemy.engine.Engine
    """
    log.debug("Retrieving the postgres db engine.")
    return create_engine(
        f"{app_env_config.POSTGRESDB_DRIVERNAME}://{app_env_config.POSTGRESDB_USERNAME}:{app_env_config.POSTGRESDB_PASSWORD.get_secret_value()}@{app_env_config.POSTGRESDB_HOST}:{app_env_config.POSTGRESDB_PORT}/{app_env_config.POSTGRESDB_DATABASE}",
        echo=app_env_config.POSTGRESDB_ECHO_LOG_LEVEL,
        future=app_env_config.POSTGRESDB_FUTURE
    )

@lru_cache(maxsize=None)
def get_postgres_db():
    """
    Retrieving the postgres db session.
    :return: A SqlAlchemy Session - sqlalchemy.orm.session.sessionmaker
    """
    log.debug("Retrieving the postgres db session.")
    postgres_session = sessionmaker(
        bind=get_postgres_db_engine(),
        autocommit=app_env_config.POSTGRESDB_SESSION_AUTOCOMMIT,
        autoflush=app_env_config.POSTGRESDB_SESSION_AUTOFLUSH,
    )

    return postgres_session()
