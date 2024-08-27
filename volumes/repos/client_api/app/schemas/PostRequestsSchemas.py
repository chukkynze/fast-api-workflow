import datetime
from typing import Optional
from pydantic import BaseModel


class CreatePostRequestDataSchema(BaseModel):
    """
    This is the data needed in the request to create a post
    """
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None


class CreatePostInsertDataSchema(BaseModel):
    """
    This is the data needed by the Posts Service to create a post
    """
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None


class GetPostResponseDataSchema(BaseModel):
    """
    This is the data needed by the Posts Service to create a post
    """
    id: int
    uuid: str
    title: str
    content: str
    published: bool
    rating: float
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime


class UpdatePostDataSchema(BaseModel):
    """
    The update schema may be different from the create schema
    because of automatically added fields from defaults and other
    means
    """
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None


class PatchDataSchema(BaseModel):
    id: int
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool] = True
    rating: Optional[float] = None

