from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status


def add_posts_exception_handlers(app: FastAPI) -> None:
    """

    :param app:
    :return:
    """

    @app.exception_handler(CreatePostFailurePostServiceException)
    async def item_not_found_exception_handler(
            request: Request,
            exc: CreatePostFailurePostServiceException
    ):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": False,
                "message": "Could not create a new Post.",
            },
        )

    @app.exception_handler(CachePostFailurePostServiceException)
    async def item_not_found_exception_handler(
            request: Request,
            exc: CachePostFailurePostServiceException
    ):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": False,
                "message": "Could not cache a newly created Post.",
            },
        )


class CreatePostFailurePostServiceException(Exception):
    def __init__(self, message: str):
        self.message = message


class CachePostFailurePostServiceException(Exception):
    def __init__(self, message: str):
        self.message = message


class PostsRepositoryInsertException(Exception):
    def __init__(self, message: str):
        self.message = message

