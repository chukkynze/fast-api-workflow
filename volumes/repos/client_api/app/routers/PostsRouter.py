from fastapi import APIRouter, Response, status
from app.log.loggers.app_logger import get_app_logger
from app.schemas.PostRequestsSchemas import CreatePostRequestDataSchema, CreatePostInsertDataSchema, UpdatePostDataSchema, PatchDataSchema
from app.services.PostService import PostService

# Logging
log = get_app_logger()

router = APIRouter(
    prefix="/posts",
    tags=["v0", "Posts"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(request_post_data: CreatePostRequestDataSchema, response: Response):

    log.debug("Hit: create_post method of PostsRouter.")

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
                "timestamp": "",
                "sent": request_post_data
            } | service_res["meta"]

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
            "meta": {
                "timestamp": "",
                "sent": request_post_data
            }
        }

    return app_response

@router.get("/", status_code=status.HTTP_200_OK)
async def get_posts():

    log.debug("Hit: get_posts method of PostsRouter.")

    service = PostService()
    service_res = service.get_posts()
    log.debug("Service response = %s", service_res)

    meta = {
                "timestamp": "",
            } | service_res["meta"]

    return {
        "status": service_res['status'],
        "message": "Successfully retrieved all posts.",
        "data": service_res['data'],
        "meta": meta,
    }









@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int):

    service = PostService()
    post = service.get_post(id)

    return {
        "status": True,
        "message": f"Successfully retrieved the post for id: {id}.",
        "data": post,
    }


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, new_post_data: UpdatePostDataSchema, response: Response):

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


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_post(id: int, new_post_data: PatchDataSchema, response: Response):

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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    service = PostService()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
