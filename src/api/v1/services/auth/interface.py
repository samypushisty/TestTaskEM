from abc import abstractmethod
from typing import Protocol

from secure import JwtInfo
from .schemas import JWTRead, GetUser, UserPatch, UserReg, UserSign, UserChangePassword
from api.v1.base_schemas.schemas import GenericResponse

class AuthServiceI(Protocol):
    @abstractmethod
    async def reg_user(self, user: UserReg) -> GenericResponse[JWTRead]:
        ...

    @abstractmethod
    async def sign_user(self, user: UserSign) -> GenericResponse[JWTRead]:
        ...

    @abstractmethod
    async def logout_user(self, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def get_user(self, user_id: int) -> GenericResponse[GetUser]:
        ...

    @abstractmethod
    async def patch_user(self, user: UserPatch, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def delete_user(self, token: JwtInfo) -> None:
        ...

    @abstractmethod
    async def update_token(self, token: JwtInfo) -> GenericResponse[JWTRead]:
        ...

    @abstractmethod
    async def edit_password(self, token: JwtInfo, user_change_password: UserChangePassword) -> None:
        ...