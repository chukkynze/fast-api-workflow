import logging
from datetime import datetime
import uuid
from typing import Annotated
from fastapi import APIRouter, Response, status
from pydantic import UUID4, AfterValidator
from app.schemas.PostRequestsSchemas import CreatePostRequestDataSchema, CreatePostInsertDataSchema, \
    UpdatePostDataSchema, PatchDataSchema
from app.services.PostService import PostService

# Logging
log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/posts",
    tags=["v0", "Posts"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
        request_post_data: CreatePostRequestDataSchema,
        response: Response
):
    started_at = datetime.now().isoformat()
    log.info("Hit: create post.")

    insert_data = {
        "title": request_post_data.title,
        "content": request_post_data.content,
        'published': request_post_data.published if 'published' in request_post_data else True,
        'rating': request_post_data.rating if 'rating' in request_post_data else 0.0,
    }
    log.debug("Processed validated request data")

    # Process (and validate) insert data
    insert_post_data = CreatePostInsertDataSchema(**insert_data)
    log.debug("Processed and validated insert data")

    service = PostService()
    service_res = service.create_post(insert_post_data)
    log.debug("Service response = %s", service_res)

    meta = {
                "started": {
                    "at": started_at,
                    "with": request_post_data
                },
                "response": {} | service_res["meta"]
            }

    if service_res["status"] is True:
        app_response = {
            "status": service_res["status"],
            "message": "Successfully created post.",
            "data": service_res["data"],
            "meta": meta
        }
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        app_response = {
            "status": service_res["status"],
            "message": "Could not create a post.",
            "data": service_res["data"],
            "errors": service_res["errors"],
            "meta": meta
        }

    return app_response

@router.get("/{post_uuid}", status_code=status.HTTP_200_OK)
async def get_post(
        post_uuid: str | UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))],
        response: Response,
        ckey: str | None = None,
):
    started_at = datetime.now().isoformat()
    log.info("Hit: get post.")

    service = PostService()
    service_res = service.get_post(uuid.UUID(str(post_uuid)), ckey)
    log.debug("Service response = %s", service_res)

    meta = {
            "started": {
                "at": started_at,
                "with": {
                    "post_uuid": post_uuid,
                    "ckey": ckey,
                }
            },
            "response": {} | service_res["meta"]
        }

    if service_res["status"] is True:
        app_response = {
            "status": service_res["status"],
            "message": "Successfully retrieved the post.",
            "data": service_res["data"],
            "meta": meta
        }
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        app_response = {
            "status": service_res["status"],
            "message": "Could not get the post.",
            "data": service_res["data"],
            "errors": service_res["errors"],
            "meta": meta
        }

    return app_response

@router.get("/", status_code=status.HTTP_200_OK)
async def get_posts(response: Response):
    started_at = datetime.now().isoformat()
    log.debug("Hit: get posts")

    service = PostService()
    service_res = service.get_posts()
    log.debug("Service response = %s", service_res)

    meta = {
            "started": {
                "at": started_at,
                "with": {}
            },
            "response": {} | service_res["meta"]
        }

    if service_res["status"] is True:
        app_response = {
            "status": service_res["status"],
            "message": "Successfully retrieved all posts.",
            "data": service_res["data"],
            "meta": meta
        }
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        app_response = {
            "status": service_res["status"],
            "message": "Could not get all post.",
            "data": service_res["data"],
            "errors": service_res["errors"],
            "meta": meta
        }

    return app_response

@router.delete("/{post_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_uuid: str | UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))],
        response: Response
):
    started_at = datetime.now().isoformat()
    log.info("Hit: delete post.")

    service = PostService()
    service_res = service.delete_post(uuid.UUID(str(post_uuid)))
    log.debug("Service response = %s", service_res)

    meta = {
            "started": {
                "at": started_at,
                "with": {
                    "post_uuid": post_uuid,
                }
            },
            "response": {} | service_res["meta"]
        }

    if service_res["status"] is True:
        app_response = Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        app_response = {
            "status": service_res["status"],
            "message": "Could not delete the post.",
            "data": service_res["data"],
            "errors": service_res["errors"],
            "meta": meta
        }

    return app_response























@router.put("/{post_uuid}", status_code=status.HTTP_200_OK)
async def update_post(
        post_uuid: str | UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))],
        new_post_data: UpdatePostDataSchema,
        response: Response
):

    service = PostService()
    service_res = service.update_post(id, new_post_data.model_dump())

    if service_res["status"] is True:
        app_response = {
            "status": service_res["status"],
            "message": "Successfully updated post.",
            "data": service_res["data"],
            "meta": {
                "timestamp": "",
                "sent": new_post_data
            }
        }
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        app_response = {
            "status": service_res["status"],
            "message": "Could not update this post.",
            "data": service_res["data"],
            "errors": service_res["errors"],
            "meta": {
                "timestamp": "",
                "sent": new_post_data
            }
        }

    return app_response


@router.patch("/{post_uuid}", status_code=status.HTTP_200_OK)
async def patch_post(
        post_uuid: str | UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))],
        new_post_data: PatchDataSchema,
        response: Response
):

    service = PostService()
    service_res = service.patch_post(id, new_post_data.model_dump())

    if service_res["status"] is True:
        app_response = {
            "status": service_res["status"],
            "message": "Successfully partially updated post.",
            "data": service_res["data"],
            "meta": {
                "timestamp": "",
                "sent": new_post_data
            }
        }
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        app_response = {
            "status": service_res["status"],
            "message": "Could not update this post.",
            "data": service_res["data"],
            "errors": service_res["errors"],
            "meta": {
                "timestamp": "",
                "sent": new_post_data
            }
        }

    return app_response

