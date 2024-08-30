import os
from enum import Enum
from functools import lru_cache

from pydantic.types import SecretStr
from pydantic_settings import BaseSettings


class AppEnvironmentEnum(str, Enum):
    development = 'development'
    dev = 'dev'
    testing = 'testing'
    test = 'test'
    acceptance = 'acceptance'
    qa = 'qa'
    production = 'production'
    prod = 'prod'


class AppLogLevelEnum(str, Enum):
    CRITICAL = "CRITICAL"
    FATAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    WARN = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


class AppSettings(BaseSettings):
    APP_ENV: AppEnvironmentEnum
    APP_LOG_LEVEL: AppLogLevelEnum
    APP_VERSION: str
    APP_PROJECT_NAME: str
    APP_PROJECT_DESCRIPTION: str

    MYSQLDB_DRIVERNAME: str
    MYSQLDB_USERNAME: str
    MYSQLDB_PASSWORD: SecretStr
    MYSQLDB_HOST: str
    MYSQLDB_PORT: int
    MYSQLDB_DATABASE: str
    MYSQLDB_ECHO_LOG_LEVEL: str
    MYSQLDB_FUTURE: bool
    MYSQLDB_SESSION_AUTOCOMMIT: bool
    MYSQLDB_SESSION_AUTOFLUSH: bool

    POSTGRESDB_DRIVERNAME: str
    POSTGRESDB_USERNAME: str
    POSTGRESDB_PASSWORD: SecretStr
    POSTGRESDB_HOST: str
    POSTGRESDB_PORT: int
    POSTGRESDB_DATABASE: str
    POSTGRESDB_ECHO_LOG_LEVEL: str
    POSTGRESDB_FUTURE: bool
    POSTGRESDB_SESSION_AUTOCOMMIT: bool
    POSTGRESDB_SESSION_AUTOFLUSH: bool

    REDIS_CACHE_DRIVERNAME: str
    REDIS_CACHE_USERNAME: str
    REDIS_CACHE_PASSWORD: SecretStr
    REDIS_CACHE_HOST: str
    REDIS_CACHE_PORT: int
    REDIS_CACHE_PRIMARY_DB: int

    REDIS_SEARCH_DRIVERNAME: str
    REDIS_SEARCH_USERNAME: str
    REDIS_SEARCH_PASSWORD: SecretStr
    REDIS_SEARCH_HOST: str
    REDIS_SEARCH_PORT: int
    REDIS_SEARCH_PRIMARY_DB: int

    REDIS_DOC_DRIVERNAME: str
    REDIS_DOC_USERNAME: str
    REDIS_DOC_PASSWORD: SecretStr
    REDIS_DOC_HOST: str
    REDIS_DOC_PORT: int
    REDIS_DOC_PRIMARY_DB: int

    REDIS_MONITOR_DRIVERNAME: str
    REDIS_MONITOR_USERNAME: str
    REDIS_MONITOR_PASSWORD: SecretStr
    REDIS_MONITOR_HOST: str
    REDIS_MONITOR_PORT: int
    REDIS_MONITOR_PRIMARY_DB: int

    REDIS_AI_DRIVERNAME: str
    REDIS_AI_USERNAME: str
    REDIS_AI_PASSWORD: SecretStr
    REDIS_AI_HOST: str
    REDIS_AI_PORT: int
    REDIS_AI_PRIMARY_DB: int

@lru_cache
def get_app_env_config():
    config = AppSettings(_env_file=os.path.join(os.path.dirname(__file__), ".env"))
    return config

