__all__ = (
    "auth_router",
    "manage_router"
)

from api.api_v1.routes.auth import router as auth_router
from api.api_v1.routes.work_with_permisiions import router as manage_router
