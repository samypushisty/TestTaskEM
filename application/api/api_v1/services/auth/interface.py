from abc import abstractmethod
from typing import Protocol

from secure import JwtInfo
from .schemas import JWTRead, GetUser, UserPatch, UserReg, UserSign
from api.api_v1.base_schemas.schemas import GenericResponse

class AuthServiceI(Protocol):
    @abstractmethod
    async def reg_user(self, user: UserReg) -> GenericResponse[JWTRead]:
        ...

    @abstractmethod
    async def sign_user(self, user: UserSign) -> GenericResponse[JWTRead]:
        ...

    @abstractmethod
    async def get_user(self, token: JwtInfo) -> GenericResponse[GetUser]:
        ...

    @abstractmethod
    async def patch_user(self, user: UserPatch, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def delete_user(self, token: JwtInfo) -> None:
        ...
