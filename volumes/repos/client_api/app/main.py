from fastapi import FastAPI, Depends, status
from app.dependencies import get_token_header
from app.config import settings
from app.routers import PostsRouter
from app.exceptions.AppExceptionHandlers import add_app_exception_handlers

app = FastAPI(
    title="Awesome API", # settings.PROJECT_NAME,
    description="This API does awesome things",
    dependencies=[Depends(get_token_header)]
)

# Exception Handlers
add_app_exception_handlers(app)

# Routes
app.include_router(PostsRouter.router)

@app.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def root():
    return {
        "status": True,
        "message": "Hello World.",
        "data": {
            "company": "AcademyStack LLC",
            "author": "Chukwuma Nze",
            "version": 0.00,
        },
        "settings": settings,
    }
