import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
from starlette import status
from app.exceptions.data.PostsExceptions import add_posts_exception_handlers


# Logging
log = logging.getLogger(__name__)


def add_app_exception_handlers(app: FastAPI) -> None:
    """
    Add exception handlers to the FastAPI app.
    Define all the exception handlers that your app needs here
    in one location.
    :param app:
    :return:
    """

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        log.error(f" Unhandled general exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": False,
                "message": f"Unhandled general exception: {exc}",
            },
        )

    @app.exception_handler(IndexError)
    async def index_error_exception_handler(request: Request, exc: IndexError):
        log.error(f" Unhandled index error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": False,
                "message": "Unhandled index error",
                "data": {
                    "err_msg": f"IndexError: {exc}"
                },
            },
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        log.error(f" A request validation exception occurred: {exc}")
        errors = exc.errors()
        err_msg = "Something went wrong."
        for error in errors:
            if error['msg']:
                err_msg = f"{error['msg']}"
                break

        output_content = {
            "status": False,
            "message": "A request validation exception occurred.",
            "data": {
                "err_msg": err_msg,
                "detail": exc.errors(),
                "body": exc.body
            },
        }

        # Add condition for metadata
        if 0 < 2:
            output_content["meta"] = {
                "requestKey": request.headers.get("X-Request-Key"),
                "timestamp": datetime.now().isoformat()
            }

        # Add config for debug
        if 0 < 1:
            output_content["debug"] = {
                "request": str(request.__dict__)
            }

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=output_content,
        )

    # Model Exceptions
    ######################

    # Posts
    add_posts_exception_handlers(app)