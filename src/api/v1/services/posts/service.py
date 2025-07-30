from api.v1.services.posts.interface import PostServiceI
from api.v1.services.posts.schemas import UserPost, GetPost, GetPosts
from api.v1.utils.repository import SQLAlchemyRepository
from api.v1.base_schemas.schemas import GenericResponse, StandartException
from core.models.base import User
from secure import JwtInfo
from typing import Callable, Optional
from sqlalchemy.ext.asyncio import AsyncSession

import sys
import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

class PostService(PostServiceI):
    def __init__(self, repository_post: SQLAlchemyRepository,repository_user: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository_post = repository_post
        self.repository_user=repository_user
        self.session = database_session

    async def add_post(self, token: JwtInfo, user_post: UserPost) -> None:
        async with self.session() as session:
            async with session.begin():
                logger.debug(f"User {token.id} start add post")
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if not work_user.has_permission("create"):
                    raise StandartException(status_code=403, detail="Forbidden")
                data = user_post.model_dump()
                data["user_id"] = token.id
                await self.repository_post.add(session=session, data=data)
                logger.debug(f"User {token.id} finish add post")

    async def get_post(self, post_id: int) -> GenericResponse[GetPost]:
        async with self.session() as session:
            async with session.begin():
                logger.debug(f"Start get post")
                result = await self.repository_post.find(session=session, table_id=post_id)
            result = GetPost.model_validate(result, from_attributes=True)
            logger.debug(f"Finish get post")
            return GenericResponse[GetPost](detail=result)

    async def get_posts(self, page: int) -> GenericResponse[GetPosts]:
        async with self.session() as session:
            async with session.begin():
                logger.debug(f"Start get posts")
                result = await self.repository_post.find_paginated(session=session,order_column="table_id",page=page)
                result = GetPosts(posts=[ GetPost.model_validate(post, from_attributes=True) for post in result])
                logger.debug(f"Start get posts")
                return GenericResponse[GetPosts](detail=result)

    async def get_user_posts(self, page: int, user_id: int) -> GenericResponse[GetPosts]:
        async with self.session() as session:
            async with session.begin():
                logger.debug(f"Start get posts user{user_id}")
                result = await self.repository_post.find_paginated(session=session, user_id=user_id, order_column="table_id",page=page)
                result = GetPosts(posts=[GetPost.model_validate(post, from_attributes=True) for post in result])
                logger.debug(f"Finish get posts user{user_id}")
                return GenericResponse[GetPosts](detail=result)

    async def delete_post(self, token: JwtInfo, post_id: int, user_id: Optional[int]) -> None:
        async with self.session() as session:
            async with session.begin():
                logger.debug(f"Start delete post {post_id} user {user_id}")
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if user_id:
                    if not work_user.has_permission("moderator") or not work_user.has_permission("delete"):
                        raise StandartException(status_code=403, detail="Forbidden")
                    logger.debug(f"Finish delete post {post_id} user {user_id}")
                    await self.repository_post.delete(session=session,user_id=user_id,table_id=post_id)
                else:
                    if not work_user.has_permission("delete"):
                        raise StandartException(status_code=403, detail="Forbidden")
                    logger.debug(f"Finish delete post {post_id} user {user_id}")
                    await self.repository_post.delete(session=session, user_id=token.id, table_id=post_id)


    async def patch_post(self, token: JwtInfo, post_id:int, user_post: UserPost, user_id: Optional[int])  -> None:
        async with self.session() as session:
            async with session.begin():
                logger.debug(f"Start patch post {post_id} user {user_id}")
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if user_id:
                    if not work_user.has_permission("moderator") or not work_user.has_permission("edit"):
                        raise StandartException(status_code=403, detail="Forbidden")
                    patch_data = user_post.model_dump(exclude_unset=True)
                    logger.debug(f"Finish patch post {post_id} user {user_id}")
                    await self.repository_post.patch(session=session, data=patch_data, user_id=user_id, table_id=post_id)
                else:
                    if not work_user.has_permission("edit"):
                        raise StandartException(status_code=403, detail="Forbidden")
                    patch_data = user_post.model_dump(exclude_unset=True)
                    logger.debug(f"Finish patch post {post_id} user {user_id}")
                    await self.repository_post.patch(session=session, data=patch_data, user_id=token.id, table_id=post_id)