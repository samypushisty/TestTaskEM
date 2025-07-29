__all__ = (
    "auth_router",
    "manage_router",
    "post_router"

)

from api.v1.routes.auth import router as auth_router
from api.v1.routes.work_with_permisiions import router as manage_router
from api.v1.routes.post import router as post_router
