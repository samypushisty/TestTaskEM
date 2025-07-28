from api.api_v1.services.work_with_permissions.interface import ManageServiceI
from api.api_v1.utils.repository import SQLAlchemyRepository
from api.api_v1.services.work_with_permissions.schemas import GetUser, PermissionShem
from api.api_v1.base_schemas.schemas import GenericResponse, StandartException
from core.models.base import User, Permission
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession


class ManageService(ManageServiceI):
    def __init__(self, repository_user: SQLAlchemyRepository,repository_permissions: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository_user = repository_user
        self.repository_permissions=repository_permissions
        self.session = database_session

    async def add_permission(self, token: JwtInfo, user_id: int, permission: str) -> None:
        async with self.session() as session:
            async with session.begin():
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if not work_user.active:
                    raise StandartException(status_code=403, detail="Not Found")
                if not work_user.has_permission("admin"):
                    raise StandartException(status_code=403, detail="Forbidden")

                permission: Permission = await self.repository_permissions.find(session=session, name=permission, validate=True)
                user: User = await self.repository_user.find(session=session, user_id=user_id, validate=True)
                if permission not in user.permissions:
                    user.permissions.append(permission)

    async def delete_permission(self, token: JwtInfo, user_id: int, permission: str) -> None:
        async with self.session() as session:
            async with session.begin():
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if not work_user.active:
                    raise StandartException(status_code=403, detail="Not Found")
                if not work_user.has_permission("admin"):
                    raise StandartException(status_code=403, detail="Forbidden")

                permission: Permission = await self.repository_permissions.find(session=session, name=permission,
                                                                                validate=True)
                user: User = await self.repository_user.find(session=session, user_id=user_id, validate=True)
                if permission in user.permissions:
                    user.permissions.remove(permission)

    async def get_user(self, token: JwtInfo, user_id: int) -> GenericResponse[GetUser]:
        async with self.session() as session:
            async with session.begin():
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if not work_user.active:
                    raise StandartException(status_code=403, detail="Not Found")
                if not work_user.has_permission("moderator"):
                    raise StandartException(status_code=403,detail="Forbidden")
                user: User = await self.repository_user.find(session=session, user_id=user_id, validate=True)
                result = GetUser(
                    user_id = user.user_id,
                    registration = user.registration,
                    last_visit = user.last_visit,
                    email = user.email,
                    name = user.name,
                    last_name = user.last_name,
                    description = user.description,
                    permissions = [
                        PermissionShem(
                            permission_id = permission.permission_id,
                            name = permission.name,
                            description = permission.description,
                        )
                        for permission in user.permissions
                    ],
                )
                return GenericResponse[GetUser](detail=result)

    async def delete_user(self, token: JwtInfo, user_id: int) -> None:
        async with self.session() as session:
            async with session.begin():
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if not work_user.active:
                    raise StandartException(status_code=403, detail="Not Found")
                if not work_user.has_permission("moderator"):
                    raise StandartException(status_code=403, detail="Forbidden")
                permission: Permission = await self.repository_permissions.find(session=session, name="admin",
                                                                                validate=True)
                user : User = await self.repository_user.find(session=session, user_id=user_id, validate=True)
                if permission in user.permissions:
                    raise StandartException(status_code=403, detail="Forbidden")
                await self.repository_user.patch_field(session=session, user_id=user_id, field="active", value=False)

    async def activate_user(self, token: JwtInfo, user_id: int) -> None:
        async with self.session() as session:
            async with session.begin():
                work_user: User = await self.repository_user.find(session=session, user_id=token.id, validate=True)
                if not work_user.active:
                    raise StandartException(status_code=403, detail="Not Found")
                if not work_user.has_permission("moderator"):
                    raise StandartException(status_code=403, detail="Forbidden")
                permission: Permission = await self.repository_permissions.find(session=session, name="admin",
                                                                                validate=True)
                user: User = await self.repository_user.find(session=session, user_id=user_id, validate=True)
                if permission in user.permissions:
                    raise StandartException(status_code=403,detail="Forbidden")
                await self.repository_user.patch_field(session=session, user_id=user_id, field="active",
                                                           value=True)