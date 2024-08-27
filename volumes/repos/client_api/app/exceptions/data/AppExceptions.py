from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status


def add_data_exception_handlers(app: FastAPI) -> None:
    """

    :param app:
    :return:
    """
    @app.exception_handler(DatabaseConnectionException)
    async def item_not_found_exception_handler(request: Request, exc: DatabaseConnectionException):

        print(exc.__dict__)

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": False,
                "message": "Service is unavailable",
                "data": {},
            },
        )


class DatabaseConnectionException(Exception):
    def __init__(self, name: str):
        self.name = name