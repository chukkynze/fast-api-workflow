import logging
import os
from fastapi import FastAPI, Depends, status
from app.dependencies import get_token_header
from app.config import config
from app.log.loggers.app_logger import get_app_logger
from app.routers import PostsRouter
from app.exceptions.AppExceptionHandlers import add_app_exception_handlers
from app.exceptions.data.AppExceptions import add_data_exception_handlers

os.environ["REDIS_OM_URL"] = "redis://client-redis-stack:6379"
app = FastAPI(
    title=config.APP_PROJECT_NAME,
    description=config.APP_PROJECT_DESCRIPTION,
    dependencies=[Depends(get_token_header)]
)

# Logging
log = get_app_logger()

# Exception Handlers
add_app_exception_handlers(app)
add_data_exception_handlers(app)

# Routes
app.include_router(PostsRouter.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    log.info("Root endpoint hit.")

    output_data = {
        "company": "AcademyStack LLC",
        "author": "Chukwuma Nze",
        "description": config.APP_PROJECT_DESCRIPTION,
    }

    if config.APP_ENV in ["development", "dev"]:
        output_data['settings'] = config.dict()

    output_meta = {
        "timestamp": "",
    }

    output = {
        "status": True,
        "message": f"{config.APP_PROJECT_NAME} is up and running.",
        "data": output_data,
        "meta": output_meta,
    }

    return output

# @app.on_event("startup")
# async def startup_event():
#     logger.info("Opening mols bakery...")
#     app.state.redis = await init_redis_pool()
#     app.state.mols_repo = MoleculesRepository(app.state.redis)
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     logger.info("Closing mols bakery...")
#     await app.state.redis.close()


@app.get("/health-check", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": True,
        "message": "But Jesus looked at them and said, “With man this is impossible, but with God all things are possible."
    }