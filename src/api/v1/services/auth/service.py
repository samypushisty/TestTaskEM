from sqlalchemy import select, Result, insert

from api.v1.services.posts.schemas import GetPost
from api.v1.utils.repository import SQLAlchemyRepository
from api.v1.services.auth.schemas import JWTRead, GetUser, UserPatch, UserSign, UserReg, UserChangePassword
from api.v1.base_schemas.schemas import GenericResponse, StandartException
from core.config import settings
from core.models.base import User, Permission, UserPermissionAssociation
from secure import create_jwt, JwtInfo
from datetime import datetime, timezone
from typing import Callable, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.services.auth.interface import AuthServiceI
from secure.hash_password import hash_password, check_password

import sys
import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

class AuthService(AuthServiceI):
    def __init__(self, repository_user: SQLAlchemyRepository, repository_settings: SQLAlchemyRepository, repository_permissions: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository_user = repository_user
        self.repository_settings = repository_settings
        self.repository_permissions = repository_permissions
        self.session = database_session


    async def reg_user(self, user: UserReg) -> GenericResponse[JWTRead]:
        async with self.session() as session:
            async with session.begin():
                logger.debug("Start reg user")
                result: User = await self.repository_user.find(session=session, email=user.email)
                if result:
                    logger.debug("Activate user")
                    check_password(stored_password=result.password, provided_password=user.password)
                    await self.repository_user.patch_field(session=session, user_id=result.user_id, field="active",
                                                           value=True)
                    logger.debug(f"End reg user {result.user_id}")
                    return GenericResponse[JWTRead](detail=JWTRead(jwt=create_jwt(result.user_id)))

                user.password = hash_password(user.password)
                data = user.model_dump(exclude_unset=True)
                user_table = await self.repository_user.add(session=session, data=data)


                #add permissions to user
                permission_query = select(Permission).where(Permission.name.in_(settings.default_permissions))
                permissions: Result = await session.execute(permission_query)
                default_permissions: Sequence[Permission] = permissions.scalars().all()
                if default_permissions:
                    stmt = insert(UserPermissionAssociation).values(
                        [{"user_id": user_table.user_id, "permission_id": perm.permission_id} for perm in
                         default_permissions]
                    )
                    await session.execute(stmt)

                #add settings to user
                user_settings = {"user_id": user_table.user_id, "theme": "auto", "language": "english",
                                 "notifications": True}
                await self.repository_settings.add(session=session, data=user_settings)
                logger.debug(f"end reg user {user_table.user_id}")
                return GenericResponse[JWTRead](detail=JWTRead(jwt=create_jwt(user_table.user_id)))

    async def sign_user(self, user: UserSign) -> GenericResponse[JWTRead]:
        async with self.session() as session:
            async with session.begin():
                logger.debug("Start sign user")
                result: User = await self.repository_user.find(session=session, email=user.email, validate=True)
                if not result.active:
                    logger.error("User not found")
                    raise StandartException(status_code=404,detail="user not found")
                check_password(stored_password=result.password,provided_password=user.password)
                await self.repository_user.patch(session=session, data={
                        "last_visit": datetime.now(timezone.utc).replace(tzinfo=None)}, user_id=result.user_id)
                logger.debug(f"End sign user {result.user_id}")
                return GenericResponse[JWTRead](detail=JWTRead(jwt=create_jwt(result.user_id)))

    async def logout_user(self, token: JwtInfo) -> None:
        token.logout()

    async def edit_password(self, token: JwtInfo, user_change_password:UserChangePassword) -> None:
        async with self.session() as session:
            async with session.begin():
                logger.debug(f"Start change password to user {token.id}")
                result: User = await self.repository_user.find(session=session, validate=True, user_id=token.id)
                check_password(stored_password=result.password, provided_password=user_change_password.old_password)
                await self.repository_user.patch_field(session=session, user_id=token.id, field="password",
                                                   value=hash_password(user_change_password.new_password))
                logger.debug(f"Finish change password to user {token.id}")

    async def get_user(self, user_id: int) -> GenericResponse[GetUser]:
        async with self.session() as session:
            async with session.begin():
                logger.debug(f"Start get user {user_id}")
                result = await self.repository_user.find(session=session, user_id=user_id, validate=True)
                result = GetUser(
                    user_id=result.user_id,
                    registration=result.registration,
                    last_visit=result.last_visit,
                    email=result.email,
                    name=result.name,
                    last_name=result.last_name,
                    description=result.description,
                    posts=[GetPost.model_validate(post, from_attributes=True) for post in result.posts],
                )
                logger.debug(f"Finish get user {user_id}")
                return GenericResponse[GetUser](detail=result)

    async def patch_user(self, user: UserPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                logger.debug(f"Start patch user {token.id}")
                patch_data = user.model_dump(exclude_unset=True)
                await self.repository_user.patch(session=session, data=patch_data, user_id=token.id)
                logger.debug(f"Finish patch user {token.id}")

    async def delete_user(self, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                logger.debug(f"Start delete user {token.id}")
                token.logout()
                await self.repository_user.patch_field(session=session, user_id=token.id, field="active", value=False)
                logger.debug(f"Finish delete user {token.id}")

    async def update_token(self, token: JwtInfo) -> GenericResponse[JWTRead]:
        logger.debug(f"Update token {token.id}")
        return GenericResponse[JWTRead](detail=JWTRead(jwt=create_jwt(token.id)))
