from abc import abstractmethod
from typing import Protocol

from secure import JwtInfo
from .schemas import UserAuth, JWTRead, GetUser
from api.api_v1.base_schemas.schemas import GenericResponse

class AuthServiceI(Protocol):
    @abstractmethod
    async def registration_user(self, user: UserAuth) -> GenericResponse[JWTRead]:
        ...

    @abstractmethod
    async def get_user(self, token: JwtInfo) -> GenericResponse[GetUser]:
        ...
