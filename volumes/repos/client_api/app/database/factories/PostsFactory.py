import factory
from datetime import datetime
from app.database.configs.dbs import get_postgres_db
from app.database.models.CustomerData.PostsModel import PostsModel


class PostsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = PostsModel
        sqlalchemy_session = get_postgres_db()   # the SQLAlchemy session object
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n+1)
    uuid = factory.Faker('uuid4', locale='en_US')
    title = factory.Faker('sentence', locale='en_US')
    content = factory.Faker('text', locale='es_ES')
    published = factory.Faker('boolean')
    rating = factory.Faker('pydecimal', left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=5.00)
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    deleted_at = None
