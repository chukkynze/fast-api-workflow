from typing import Any, Optional
from pydantic import BaseModel


class RepoResponse(BaseModel):
    status: bool
    message: Optional[str] = None
    data: Any
    errors: dict
    meta: Optional[dict] = None


class BaseAppRepository:
    def __init__(self):
        pass