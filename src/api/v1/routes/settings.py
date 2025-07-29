from fastapi import APIRouter, Depends
from api.v1.services.settings import UserSettingsServiceI
from api.v1.container import container
from api.v1.base_schemas.schemas import GenericResponse
from api.v1.services.settings.schemas import UserSettingsPatch, UserSettingsRead
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(tags=["UserSettings"])

async def get_user_settings_service() -> UserSettingsServiceI:
    return container.user_settings_service()

@router.patch("")
async def patch_settings(
        user_settings: UserSettingsPatch,
        token: JwtInfo = Depends(validation),
        user_settings_service = Depends(get_user_settings_service),
        ):
    await user_settings_service.patch_settings(user_settings=user_settings,token=token)


@router.get("",response_model=GenericResponse[UserSettingsRead])
async def get_settings(
        token: JwtInfo = Depends(validation),
        user_settings_service = Depends(get_user_settings_service),
        ):
    return await user_settings_service.get_settings(token=token)