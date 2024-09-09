import sys
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from app.database.configs.dbs import get_postgres_db_engine
from app.database.factories.PostsFactory import PostsFactory


Base = declarative_base()
env = sys.argv[1]


def posts_table_seeder():
    # PostgresDB

    with get_postgres_db_engine().connect() as connection:
        connection.execute(text("TRUNCATE TABLE posts"))
        connection.commit()
        connection.execute(text("SELECT setval('posts_id_seq', max(id)+1) FROM posts;"))

    PostsFactory.create_batch(5)

    # MySQLDB
    # Base.metadata.drop_all(get_mysql_db_engine(), tables=[PostsModel.__table__])
    # Base.metadata.create_all(get_mysql_db(), tables=[PostsModel.__table__])
    # PostsFactory.create_batch(5)
