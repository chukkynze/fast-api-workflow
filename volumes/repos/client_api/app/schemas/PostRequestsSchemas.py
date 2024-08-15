from typing import Optional
from pydantic import BaseModel


class CreatePostDataSchema(BaseModel):
    """
    This is the minimum data needed in a request to create a post
    """
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None


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

