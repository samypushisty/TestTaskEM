from abc import abstractmethod
from typing import Protocol

from secure import JwtInfo
from .schemas import GetUser
from api.api_v1.base_schemas.schemas import GenericResponse

class ManageServiceI(Protocol):
    @abstractmethod
    async def add_permission(self, token: JwtInfo, user_id: int, permission: str) -> None:
        ...

    @abstractmethod
    async def delete_permission(self, token: JwtInfo, user_id: int, permission: str) -> None:
        ...

    @abstractmethod
    async def get_user(self, token: JwtInfo, user_id: int) -> GenericResponse[GetUser]:
        ...

    @abstractmethod
    async def delete_user(self, token: JwtInfo, user_id: int) -> None:
        ...

    @abstractmethod
    async def activate_user(self, token: JwtInfo, user_id: int) -> None:
        ...
