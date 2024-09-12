import datetime
from typing import Optional
from pydantic import BaseModel


class AppResponse(BaseModel):
    """
    This is the format model for all responses from this API.
    """
    status: bool
    message: str
    data: dict | list | bool | str = {}
    errors: dict = None
    meta: dict = {}