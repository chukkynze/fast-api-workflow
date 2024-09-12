import datetime
import logging
import os
import json
from fastapi import FastAPI, Depends, status
from redis_om import Migrator
from app.dependencies import get_x_token_header, get_accept_version_header
from app.exceptions.AppExceptionHandlers import add_app_exception_handlers
from app.exceptions.data.AppExceptions import add_data_exception_handlers
from app.log.loggers.app_logger import get_app_logger
from app.routers import PostsRouter
from app.schemas.AppSchemas import AppResponse
from config import get_app_env_config

app_env_config = get_app_env_config()

app = FastAPI(
    title=app_env_config.APP_PROJECT_NAME,
    description=app_env_config.APP_PROJECT_DESCRIPTION,
    dependencies=[Depends(get_x_token_header), Depends(get_accept_version_header)]
)

# Logging
get_app_logger()
log = logging.getLogger(__name__)

# Exception Handlers
add_app_exception_handlers(app)
add_data_exception_handlers(app)

# Routes
app.include_router(PostsRouter.router)

# Redis Cache models
Migrator().run()


@app.get("/", status_code=status.HTTP_200_OK, response_model=AppResponse)
async def root():
    log.info("HIT: Root.")

    output_data = {
        "company": "AcademyStack LLC",
        "author": "Chukwuma Nze",
        "description": app_env_config.APP_PROJECT_DESCRIPTION,
    }

    if app_env_config.APP_ENV in ["development", "dev"] and app_env_config.APP_LOG_LEVEL == "DEBUG":
        output_data['settings'] = json.loads(app_env_config.model_dump_json())

    output_meta = {
        "timestamp": datetime.datetime.now().isoformat(),
        "environment": app_env_config.APP_ENV,
        "commit_hash": os.getenv("COMMIT_HASH", "N/A"),
        "build_tag": os.getenv("BUILD_TAG", "N/A"),
        "build_url": os.getenv("BUILD_URL", "N/A"),
        "app_version": app_env_config.APP_VERSION,
        "os": {
            "system": os.name,
            "release": os.uname().release,
            "version": os.uname().version,
        }
    }

    output = {
        "status": True,
        "message": f"{app_env_config.APP_PROJECT_NAME} is up and running.",
        "data": output_data,
        "meta": output_meta,
    }

    return AppResponse(**output)


@app.get("/health-check", status_code=status.HTTP_200_OK, response_model=AppResponse)
async def health_check():
    log.info("HIT: Health Check")

    return AppResponse(
        status=True,
        message="Health check endpoint is up and running.",
        data="But Jesus looked at them and said, \"With man this is impossible, but with God all things are possible\"."
    )
