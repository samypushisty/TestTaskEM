from api.v1.services.settings.interface import UserSettingsServiceI
from api.v1.utils.repository import SQLAlchemyRepository
from api.v1.base_schemas.schemas import GenericResponse
from api.v1.services.settings.schemas import UserSettingsRead, UserSettingsPatch
from secure import JwtInfo
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession


class UserSettingsService(UserSettingsServiceI):
    def __init__(self,repository: SQLAlchemyRepository, database_session:Callable[..., AsyncSession]) -> None:
        self.repository = repository
        self.session = database_session

    async def patch_settings(self, user_settings: UserSettingsPatch,
        token: JwtInfo) -> None:
        async with self.session() as session:
            async with session.begin():
                await self.repository.patch(session=session, data=user_settings.model_dump(exclude_unset=True), user_id=token.id)


    async def get_settings(self, token: JwtInfo) -> GenericResponse[UserSettingsRead]:
        async with self.session() as session:
            result = await self.repository.find(session=session, validate=True,
                                                user_id=token.id)
        result = UserSettingsRead.model_validate(result,from_attributes=True)
        return GenericResponse[UserSettingsRead](detail=result)