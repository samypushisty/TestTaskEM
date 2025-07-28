from sqlalchemy import select, Result, insert
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.auth.schemas import JWTRead, GetUser, UserPatch, UserSign, UserReg
from api.api_v1.base_schemas.schemas import GenericResponse, StandartException
from core.config import settings
from core.models.base import User, Permission, UserPermissionAssociation
from secure import create_jwt, JwtInfo
from datetime import datetime, timezone
from typing import Callable, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.auth.interface import AuthServiceI
from secure.hash_password import hash_password, check_password


class AuthService(AuthServiceI):
    def __init__(self, repository_user: SQLAlchemyRepository, repository_settings: SQLAlchemyRepository, repository_permissions: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository_user = repository_user
        self.repository_settings = repository_settings
        self.repository_permissions = repository_permissions
        self.session = database_session


    async def reg_user(self, user: UserReg) -> GenericResponse[JWTRead]:
        async with self.session() as session:
            async with session.begin():
                result: User = await self.repository_user.find(session=session, email=user.email)
                if result:
                    print("check")
                    check_password(stored_password=result.password, provided_password=user.password)
                    await self.repository_user.patch_field(session=session, user_id=result.user_id, field="active",
                                                           value=True)
                    return GenericResponse[JWTRead](detail=JWTRead(jwt=create_jwt(result.user_id)))

                user.password = hash_password(user.password)
                user_table = await self.repository_user.add(session=session, data=user.model_dump())


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
                return GenericResponse[JWTRead](detail=JWTRead(jwt=create_jwt(user_table.user_id)))

    async def sign_user(self, user: UserSign) -> GenericResponse[JWTRead]:
        async with self.session() as session:
            async with session.begin():
                result: User = await self.repository_user.find(session=session, email=user.email, validate=True)
                if not result.active:
                    raise StandartException(status_code=404,detail="user not found")
                check_password(stored_password=result.password,provided_password=user.password)
                await self.repository_user.patch(session=session, data={
                        "last_visit": datetime.now(timezone.utc).replace(tzinfo=None)}, user_id=result.user_id)
                return GenericResponse[JWTRead](detail=JWTRead(jwt=create_jwt(result.user_id)))

    async def logout_user(self, token: JwtInfo) -> None:
        token.logout()

    async def get_user(self, user_id: int) -> GenericResponse[GetUser]:
        async with self.session() as session:
            async with session.begin():
                result = await self.repository_user.find(session=session, user_id=user_id, validate=True)
                result = GetUser.model_validate(result, from_attributes=True)
                return GenericResponse[GetUser](detail=result)

    async def patch_user(self, user: UserPatch, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                patch_data = user.model_dump(exclude_unset=True)
                await self.repository_user.patch(session=session, data=patch_data, user_id=token.id)

    async def delete_user(self, token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository_user.patch_field(session=session, user_id=token.id, field="active", value=False)
