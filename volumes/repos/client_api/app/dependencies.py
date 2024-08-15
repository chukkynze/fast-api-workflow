from typing import Annotated
from fastapi import Header, HTTPException, status


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid")

async def filter_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}