from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.auth.schemas import UserAuth, JWTRead, GetUser
from api.api_v1.base_schemas.schemas import GenericResponse
from core.models.base import User
from secure import create_jwt, JwtInfo
from datetime import datetime, timezone
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.auth.interface import AuthServiceI
from secure.hash_password import hash_password, check_password


class AuthService(AuthServiceI):
    def __init__(self, repository_user: SQLAlchemyRepository, repository_settings: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository_user = repository_user
        self.repository_settings = repository_settings
        self.session = database_session


    async def auth_user(self, user: UserAuth) -> GenericResponse[JWTRead]:
        async with self.session() as session:
            async with session.begin():
                result: User = await self.repository_user.find(session=session, chat_id=user.chat_id)
                if result:
                    check_password(stored_password=result.password,provided_password=user.password)
                    await self.repository_user.patch(session=session, data={
                        "last_visit": datetime.now(timezone.utc).replace(tzinfo=None)}, chat_id=user.chat_id)
                    return GenericResponse[JWTRead](detail=JWTRead(jwt=create_jwt(user.chat_id)))

                user_settings = {"chat_id": user.chat_id, "theme": "auto", "language": "english",
                                 "notifications": True}
                user.password = hash_password(user.password)
                await self.repository_user.add(session=session, data=user.model_dump())
                await self.repository_settings.add(session=session, data=user_settings)
                return GenericResponse[JWTRead](detail=JWTRead(jwt=create_jwt(user.chat_id)))



    async def get_user(self, token: JwtInfo) -> GenericResponse[GetUser]:
        async with self.session() as session:
            async with session.begin():
                result = await self.repository_user.find(session=session, chat_id=token.id, validate=True)
                result = GetUser.model_validate(result, from_attributes=True)
                return GenericResponse[GetUser](detail=result)