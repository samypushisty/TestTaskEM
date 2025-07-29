from api.v1.services.posts.interface import PostServiceI
from api.v1.services.posts.schemas import UserPost, GetPost, GetPosts
from api.v1.utils.repository import SQLAlchemyRepository
from api.v1.base_schemas.schemas import GenericResponse, StandartException
from core.models.base import User
from secure import JwtInfo
from typing import Callable, Optional
from sqlalchemy.ext.asyncio import AsyncSession


class PostService(PostServiceI):
    def __init__(self, repository_post: SQLAlchemyRepository,repository_user: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository_post = repository_post
        self.repository_user=repository_user
        self.session = database_session

    async def add_post(self, token: JwtInfo, user_post: UserPost) -> None:
        async with self.session() as session:
            async with session.begin():
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if not work_user.has_permission("create"):
                    raise StandartException(status_code=403, detail="Forbidden")
                data = user_post.model_dump()
                data["user_id"] = token.id
                await self.repository_post.add(session=session, data=data)

    async def get_post(self, post_id: int) -> GenericResponse[GetPost]:
        async with self.session() as session:
            async with session.begin():
                result = await self.repository_post.find(session=session, table_id=post_id)
            result = GetPost.model_validate(result, from_attributes=True)
            return GenericResponse[GetPost](detail=result)

    async def get_posts(self) -> GenericResponse[GetPosts]:
        async with self.session() as session:
            async with session.begin():
                result = await self.repository_post.find_all(session=session,order_column="table_id")
                result = GetPosts(posts=[ GetPost.model_validate(post, from_attributes=True) for post in result])
                return GenericResponse[GetPosts](detail=result)

    async def get_user_posts(self, user_id: int) -> GenericResponse[GetPosts]:
        async with self.session() as session:
            async with session.begin():

                result = await self.repository_post.find_all(session=session, user_id=user_id, order_column="table_id")
                result = GetPosts(posts=[GetPost.model_validate(post, from_attributes=True) for post in result])
                return GenericResponse[GetPosts](detail=result)

    async def delete_post(self, token: JwtInfo, post_id: int, user_id: Optional[int]) -> None:
        async with self.session() as session:
            async with session.begin():
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if user_id:
                    if not work_user.has_permission("moderator") or not work_user.has_permission("delete"):
                        raise StandartException(status_code=403, detail="Forbidden")
                    await self.repository_post.delete(session=session,user_id=user_id,table_id=post_id)
                else:
                    if not work_user.has_permission("delete"):
                        raise StandartException(status_code=403, detail="Forbidden")
                    await self.repository_post.delete(session=session, user_id=token.id, table_id=post_id)


    async def patch_post(self, token: JwtInfo, post_id:int, user_post: UserPost, user_id: Optional[int])  -> None:
        async with self.session() as session:
            async with session.begin():
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if user_id:
                    if not work_user.has_permission("moderator") or not work_user.has_permission("edit"):
                        raise StandartException(status_code=403, detail="Forbidden")
                    patch_data = user_post.model_dump(exclude_unset=True)
                    await self.repository_post.patch(session=session, data=patch_data, user_id=user_id, table_id=post_id)
                else:
                    if not work_user.has_permission("edit"):
                        raise StandartException(status_code=403, detail="Forbidden")
                    patch_data = user_post.model_dump(exclude_unset=True)
                    await self.repository_post.patch(session=session, data=patch_data, user_id=token.id, table_id=post_id)