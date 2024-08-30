from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status


def add_posts_exception_handlers(app: FastAPI) -> None:
    """

    :param app:
    :return:
    """

    @app.exception_handler(CreationException)
    async def post_not_created_exception_handler(
            request: Request,
            exc: CreationException
    ):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": False,
                "message": "Could not create a new Post.",
            },
        )

    @app.exception_handler(CacheException)
    async def post_not_cached_exception_handler(
            request: Request,
            exc: CacheException
    ):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": False,
                "message": "Could not cache a Post.",
            },
        )

    @app.exception_handler(ReadOneException)
    async def post_not_read_exception_handler(
            request: Request,
            exc: ReadOneException
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": False,
                "message": "Could not retrieve a Post. Check the uuid and/or cache key. Also, try removing the key.",
            },
        )

    @app.exception_handler(ReadOneCachedException)
    async def cached_post_not_read_exception_handler(
            request: Request,
            exc: ReadOneCachedException
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": False,
                "message": "Could not retrieve a cached Post.",
            },
        )

    @app.exception_handler(CacheKeyPostUuidMismatchException)
    async def cache_key_post_uuid_mismatch_exception_handler(
            request: Request,
            exc: CacheKeyPostUuidMismatchException
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "message": "The uuid sent does not match the uuid retrieved from the model found with the cache key sent.",
            },
        )


class CreationException(Exception):
    def __init__(self, message: str):
        self.message = message


class CacheException(Exception):
    def __init__(self, message: str):
        self.message = message


class ReadOneException(Exception):
    def __init__(self, message: str):
        self.message = message


class ReadOneCachedException(Exception):
    def __init__(self, message: str):
        self.message = message


class CacheKeyPostUuidMismatchException(Exception):
    def __init__(self, message: str):
        self.message = message


class GetCachedPostFailurePostServiceException(Exception):
    def __init__(self, message: str):
        self.message = message


class InsertException(Exception):
    def __init__(self, message: str):
        self.message = message


class StorageException(Exception):
    def __init__(self, message: str):
        self.message = message


class DeletePostFailurePostServiceException(Exception):
    def __init__(self, message: str):
        self.message = message

