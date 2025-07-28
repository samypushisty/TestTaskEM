from fastapi import APIRouter, Depends
from api.api_v1.container import container
from api.api_v1.services.work_with_permissions.schemas import GetUser
from api.api_v1.base_schemas.schemas import GenericResponse
from api.api_v1.services.work_with_permissions import ManageServiceI
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(tags=["Manage"])

async def get_manage_service() -> ManageServiceI:
    return container.manage_service()

@router.post("/permission")
async def get_user(
        user_id: int,
        permission: str,
        token: JwtInfo = Depends(validation),
        manage_service = Depends(get_manage_service),
        ):
    return await manage_service.add_permission(token=token, user_id=user_id, permission=permission)

@router.delete("/permission")
async def get_user(
        user_id: int,
        permission: str,
        token: JwtInfo = Depends(validation),
        manage_service = Depends(get_manage_service),
        ):
    return await manage_service.delete_permission(token=token, user_id=user_id, permission=permission)


@router.get("/user",response_model=GenericResponse[GetUser])
async def get_user(
        user_id: int,
        token: JwtInfo = Depends(validation),
        manage_service = Depends(get_manage_service),
        ):
    return await manage_service.get_user(token=token, user_id=user_id)

@router.delete("/user")
async def delete_user(
        user_id: int,
        token: JwtInfo = Depends(validation),
        manage_service = Depends(get_manage_service),
        ):
    return await manage_service.delete_user(token=token, user_id=user_id)

@router.post("/user")
async def activate_user(
        user_id: int,
        token: JwtInfo = Depends(validation),
        manage_service = Depends(get_manage_service),
        ):
    return await manage_service.activate_user(token=token, user_id=user_id)
