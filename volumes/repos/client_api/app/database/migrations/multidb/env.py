from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.config import config as envConfig

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

resource_identifier = config.config_ini_section # active config ini section is the db name that we have chosen

match resource_identifier:
    case "clientdb":
        db_name = "clientdb"
        conn_uri = f"{envConfig.MYSQLDB_DRIVERNAME}://{envConfig.MYSQLDB_USERNAME}:{envConfig.MYSQLDB_PASSWORD.get_secret_value()}@{envConfig.MYSQLDB_HOST}:{envConfig.MYSQLDB_PORT}/{envConfig.MYSQLDB_DATABASE}"
    case "customerdb":
        db_name = "customerdb"
        conn_uri = f"{envConfig.POSTGRESDB_DRIVERNAME}://{envConfig.POSTGRESDB_USERNAME}:{envConfig.POSTGRESDB_PASSWORD.get_secret_value()}@{envConfig.POSTGRESDB_HOST}:{envConfig.POSTGRESDB_PORT}/{envConfig.POSTGRESDB_DATABASE}"
    case "clientcache":
        db_name = "clientcache"
        conn_uri = f"{envConfig.REDIS_CACHE_DRIVERNAME}://{envConfig.REDIS_CACHE_USERNAME}:{envConfig.REDIS_CACHE_PASSWORD.get_secret_value()}@{envConfig.REDIS_CACHE_HOST}:{envConfig.REDIS_CACHE_PORT}"
    case _:
        raise Exception("Why are you even here? Eh?!")

config.set_main_option("sqlalchemy.url", conn_uri)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    def include_object(object, name, type_, reflected, compare_to):
        if type_ == 'foreign_key_constraint' and compare_to and (
                compare_to.elements[0].target_fullname == db_name + '.' +
                object.elements[0].target_fullname or
                db_name + '.' + compare_to.elements[0].target_fullname == object.elements[0].target_fullname):
            return False
        if type_ == 'table':
            if object.schema == db_name or object.schema is None:
                return True
        elif object.table.schema == db_name or object.table.schema is None:
            return True
        else:
            return False

    with connectable.connect() as connection:
        context.configure(
            connection=connection,target_metadata=target_metadata,include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()