from fastapi import APIRouter, Depends
from api.api_v1.container import container
from api.api_v1.services.auth import AuthServiceI
from api.api_v1.services.auth.schemas import JWTRead, GetUser, UserPatch, UserSign, UserReg
from api.api_v1.base_schemas.schemas import GenericResponse
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(tags=["User"])

async def get_auth_service() -> AuthServiceI:
    return container.auth_service()

@router.post("/reg",response_model=GenericResponse[JWTRead])
async def reg_user(
        user: UserReg,
        auth_service = Depends(get_auth_service),
        ):
    return await auth_service.reg_user(user=user)

@router.post("/sign",response_model=GenericResponse[JWTRead])
async def sign_user(
        user: UserSign,
        auth_service = Depends(get_auth_service),
        ):
    return await auth_service.sign_user(user=user)

@router.post("/logout")
async def logout_user(
        token: JwtInfo = Depends(validation),
        auth_service = Depends(get_auth_service),
        ):
    return await auth_service.logout_user(token=token)

@router.get("",response_model=GenericResponse[GetUser])
async def get_user(
        user_id: int,
        auth_service = Depends(get_auth_service),
        ):
    return await auth_service.get_user(user_id=user_id)

@router.patch("")
async def patch_user(
        user: UserPatch,
        token: JwtInfo = Depends(validation),
        auth_service = Depends(get_auth_service),
        ):
    return await auth_service.patch_user(token=token,user=user)

@router.delete("")
async def delete_user(
        token: JwtInfo = Depends(validation),
        auth_service = Depends(get_auth_service),
        ):
    return await auth_service.delete_user(token=token)

@router.post("/refresh_token",response_model=GenericResponse[JWTRead])
async def reg_user(
        token: JwtInfo = Depends(validation),
        auth_service = Depends(get_auth_service),
        ):
    return await auth_service.update_token(token=token)
