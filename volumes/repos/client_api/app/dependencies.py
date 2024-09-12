from typing import Annotated
from fastapi import Header, HTTPException, status


async def get_x_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The X-Token header is invalid")

async def get_accept_version_header(accept_version: Annotated[str, Header()]):
    if accept_version != "0.0.1":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The acceptable version requested via the header is invalid or has been deprecated.")

async def filter_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}