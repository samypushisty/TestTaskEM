from dependency_injector import containers
from dependency_injector.providers import Singleton, Factory, Resource
from api.api_v1.services.auth import AuthService, AuthServiceI

from api.api_v1.utils.repository import SQLAlchemyRepository
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from core.models.base import User, UserSettings
from core.models.db_helper import DatabaseHelper
from core.redis_db.redis_helper import redis_session_getter

class DependencyContainer(containers.DeclarativeContainer):

    database_helper: Singleton["DatabaseHelper"] = Singleton(
        DatabaseHelper,
        url=str(settings.db.url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )
    database_session: Resource["AsyncGenerator[AsyncSession, None]"] = Resource(database_helper.provided.session_getter)

    user_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model = User,
    )

    user_settings_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model=UserSettings,
    )

    auth_service: Factory["AuthServiceI"] = Factory(AuthService,
                                                    repository_user=user_repository,
                                                    repository_settings= user_settings_repository,
                                                    database_session=database_session)

container = DependencyContainer()