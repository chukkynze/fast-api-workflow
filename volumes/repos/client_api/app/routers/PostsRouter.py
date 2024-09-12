import logging
import uuid
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Response, status
from pydantic import UUID4, AfterValidator
from app.schemas.AppSchemas import AppResponse
from app.schemas.PostRequestsSchemas import (
    CreatePostRequestDataSchema,
    CreatePostInsertDataSchema,
    PatchDataSchema
)
from app.services.PostService import PostService

#
#    Especially for here, implement middleware that ensures request handling
#    fails after one second. Implement in code (req timeouts) and
#    in platform (k8s proxy-send-timeout). Also do this with databases and caches.
#   Of course use k6 to test out load and implement ddos protection
#

# Logging
log = logging.getLogger(__name__)


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
        request_post_data: CreatePostRequestDataSchema,
        response: Response
):
    started_at = datetime.now().isoformat()
    log.info("HIT: create post.")

    insert_data = {
        "title": request_post_data.title,
        "content": request_post_data.content,
        'published': request_post_data.published if 'published' in request_post_data else True,
        'rating': request_post_data.rating if 'rating' in request_post_data else 0.0,
    }

    # Process (and validate) insert data
    insert_post_data = CreatePostInsertDataSchema(**insert_data)

    service = PostService()
    service_res = service.create_post(insert_post_data)
    meta = {
        "started": {
            "at": started_at,
            "with": request_post_data
        },
        "response": {} | service_res.meta
    }

    if service_res.status is True:
        message = "Successfully created post."
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        message = "Could not create a post."

    return AppResponse(
        status=service_res.status,
        message=message,
        data=service_res.data,
        errors=service_res.errors,
        meta=meta
    )


@router.get("/{post_uuid}", status_code=status.HTTP_200_OK)
async def get_post(
        post_uuid: str | UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))],
        response: Response,
        ckey: str | None = None,
):
    started_at = datetime.now().isoformat()
    log.info("HIT: get post.")

    service = PostService()
    service_res = service.get_post(uuid.UUID(str(post_uuid)), ckey)
    meta = {
            "started": {
                "at": started_at,
                "with": {
                    "post_uuid": post_uuid,
                    "ckey": ckey,
                }
            },
            "response": {} | service_res.meta
        }

    if service_res.status is True:
        message = f"Successfully retrieved the post identified by uuid: {post_uuid}."
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        message = f"Could not retrieve the post identified by uuid: {post_uuid}."

    return AppResponse(
        status=service_res.status,
        message=message,
        data=service_res.data,
        errors=service_res.errors,
        meta=meta
    )


@router.get("/", status_code=status.HTTP_200_OK, response_model=AppResponse)
async def get_posts(
        response: Response
):
    started_at = datetime.now().isoformat()
    log.info("HIT: get posts")

    service = PostService()
    service_res = service.get_posts()
    meta = {
            "started": {
                "at": started_at,
                "with": {}
            },
            "response": {} | service_res.meta
        }

    if service_res.status is True:
        message = "Successfully retrieved all posts."
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        message = "Could not retrieve all posts."

    return AppResponse(
        status=service_res.status,
        message=message,
        data=service_res.data,
        errors=service_res.errors,
        meta=meta
    )


@router.delete("/{post_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_uuid: str | UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))],
        response: Response
):
    started_at = datetime.now().isoformat()
    log.info("HIT: delete post.")

    service = PostService()
    service_res = service.delete_post(uuid.UUID(str(post_uuid)))
    meta = {
            "started": {
                "at": started_at,
                "with": {
                    "post_uuid": post_uuid,
                }
            },
            "response": {} | service_res.meta
        }

    if service_res.status is True:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return AppResponse(
            status=service_res.status,
            message=f"Could not delete the post identified by uuid: {post_uuid}.",
            data=service_res.data,
            errors=service_res.errors,
            meta=meta
        )


@router.patch("/{post_uuid}", status_code=status.HTTP_200_OK)
async def patch_post(
        post_uuid: str | UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))],
        patch_post_data: PatchDataSchema,
        response: Response
):
    started_at = datetime.now().isoformat()
    log.info("HIT: patch post.")

    service = PostService()
    service_res = service.patch_post(uuid.UUID(str(post_uuid)), patch_post_data)
    meta = {
            "started": {
                "at": started_at,
                "with": {
                    "post_uuid": post_uuid,
                }
            },
            "response": {} | service_res.meta
        }

    if service_res.status is True:
        message = f"Successfully updated the post identified by uuid: {post_uuid}."
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        message = f"Could not update the post identified by uuid: {post_uuid}."

    return AppResponse(
        status=service_res.status,
        message=message,
        data=service_res.data,
        errors=service_res.errors,
        meta=meta
    )
