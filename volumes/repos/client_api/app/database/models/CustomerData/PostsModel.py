import uuid
from sqlalchemy import Column, String, Integer, Boolean, Float, TIMESTAMP, Uuid
#from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database.models.BaseModel import BaseAppModel


class PostsModel(BaseAppModel):
    # __table_args__ = ({'schema': 'customerdb.public'}) #db name
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    uuid = Column(Uuid(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    rating = Column(Float, default=0.0, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('null'))