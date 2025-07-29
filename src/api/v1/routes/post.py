from typing import Optional

from fastapi import APIRouter, Depends
from api.v1.container import container
from api.v1.services.posts import PostServiceI
from api.v1.services.posts.schemas import UserPost, GetPost, GetPosts
from api.v1.base_schemas.schemas import GenericResponse
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(tags=["Post"])

async def get_post_service() -> PostServiceI:
    return container.post_service()

@router.post("")
async def post_post(
        user_post: UserPost,
        token: JwtInfo = Depends(validation),
        manage_service = Depends(get_post_service),
        ):
    return await manage_service.add_post(token=token, user_post=user_post)

@router.get("")
async def get_post(
        post_id: int,
        manage_service = Depends(get_post_service),
        ):
    return await manage_service.get_post(post_id=post_id)

@router.get("/all", response_model=GenericResponse[GetPosts])
async def get_posts(
        manage_service = Depends(get_post_service),
        ):
    return await manage_service.get_posts()

@router.get("/userall", response_model=GenericResponse[GetPosts])
async def get_user_posts(
        user_id: int,
        manage_service = Depends(get_post_service),
        ):
    return await manage_service.get_user_posts(user_id=user_id)

@router.delete("")
async def delete_post(
        post_id: int,
        user_id: Optional[int] = None,
        token: JwtInfo = Depends(validation),
        manage_service = Depends(get_post_service),
        ):
    return await manage_service.delete_post(token=token, post_id=post_id, user_id=user_id)

@router.patch("")
async def patch_post(
        post_id: int,
        user_post: UserPost,
        user_id: Optional[int] = None,
        token: JwtInfo = Depends(validation),
        manage_service = Depends(get_post_service),
        ):
    return await manage_service.patch_post(token=token, user_post=user_post, post_id=post_id, user_id=user_id)
