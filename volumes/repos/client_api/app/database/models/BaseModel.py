from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

class BaseAppModel(BaseModel):
    __abstract__ = True