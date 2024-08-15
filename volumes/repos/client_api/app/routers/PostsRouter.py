from fastapi import APIRouter, Response, status
from app.schemas.PostRequestsSchemas import CreatePostDataSchema, UpdatePostDataSchema, PatchDataSchema
from app.services.PostService import PostService

router = APIRouter(
    prefix="/posts",
    tags=["v0", "Posts"],
)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int):

    service = PostService()
    post = service.get_post(id)

    return {
        "status": True,
        "message": f"Successfully retrieved the post for id: {id}.",
        "data": post,
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def get_posts():

    service = PostService()
    posts = service.get_posts()

    return {
        "status": True,
        "message": "Successfully retrieved all posts.",
        "data": posts,
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(new_post_data: CreatePostDataSchema, response: Response):

    service = PostService()
    service_res = service.create_post(new_post_data.model_dump())

    if service_res["status"] is True:
        app_response = {
            "status": service_res["status"],
            "message": "Successfully created post.",
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
            "message": "Could not create a post.",
            "data": service_res["data"],
            "errors": service_res["errors"],
            "meta": {
                "timestamp": "",
                "sent": new_post_data
            }
        }

    return app_response


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
