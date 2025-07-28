from abc import abstractmethod
from typing import Protocol, Optional

from secure import JwtInfo
from .schemas import UserPost, GetPost, GetPosts
from api.api_v1.base_schemas.schemas import GenericResponse

class PostServiceI(Protocol):
    @abstractmethod
    async def add_post(self, token: JwtInfo, user_post: UserPost) -> None:
        ...

    @abstractmethod
    async def get_post(self, post_id: int) -> GenericResponse[GetPost]:
        ...

    @abstractmethod
    async def get_posts(self) -> GenericResponse[GetPosts]:
        ...

    @abstractmethod
    async def get_user_posts(self, user_id: int) -> GenericResponse[GetPosts]:
        ...

    @abstractmethod
    async def delete_post(self, token: JwtInfo, post_id: int, user_id: Optional[int]) -> None:
        ...

    @abstractmethod
    async def patch_post(self, token: JwtInfo, post_id: int, user_post: UserPost, user_id: Optional[int]) -> None:
        ...
