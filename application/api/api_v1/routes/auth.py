from fastapi import APIRouter, Depends
from api.api_v1.container import container
from api.api_v1.services.auth import AuthServiceI
from api.api_v1.services.auth.schemas import UserAuth, JWTRead, GetUser
from api.api_v1.base_schemas.schemas import GenericResponse
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(tags=["Auth"])

async def get_auth_service() -> AuthServiceI:
    return container.auth_service()

@router.post("",response_model=GenericResponse[JWTRead])
async def auth_user(
        user: UserAuth,
        auth_service = Depends(get_auth_service),
        ):
    return await auth_service.auth_user(user=user)

@router.get("",response_model=GenericResponse[GetUser])
async def registration_user(
        token: JwtInfo = Depends(validation),
        auth_service = Depends(get_auth_service),
        ):
    return await auth_service.get_user(token=token)