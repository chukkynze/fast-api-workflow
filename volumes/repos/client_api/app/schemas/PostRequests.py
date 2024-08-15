from typing import Optional
from pydantic import BaseModel


class CreatePostDataSchema(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None


class UpdatePostDataSchema(BaseModel):
    id: int
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

