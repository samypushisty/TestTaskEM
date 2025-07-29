from dependency_injector import containers
from dependency_injector.providers import Singleton, Factory, Resource

from api.v1.services.posts import PostService, PostServiceI
from api.v1.services.auth import AuthService, AuthServiceI
from api.v1.services.permissions import ManageService, ManageServiceI
from api.v1.services.settings import UserSettingsService, UserSettingsServiceI

from api.v1.utils.repository import SQLAlchemyRepository
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from core.models.base import User, UserSettings, Permission, Post
from core.models.db_helper import DatabaseHelper

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

    user_permissions_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model=Permission,
    )

    post_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model=Post,
    )

    auth_service: Factory["AuthServiceI"] = Factory(AuthService,
                                                    repository_user=user_repository,
                                                    repository_settings= user_settings_repository,
                                                    repository_permissions=user_permissions_repository,
                                                    database_session=database_session)

    user_settings_service: Factory["UserSettingsServiceI"] = Factory(UserSettingsService,
                                                    repository=user_settings_repository,
                                                    database_session=database_session)

    manage_service: Factory["ManageServiceI"] = Factory(ManageService,
                                                    repository_user=user_repository,
                                                    repository_permissions=user_permissions_repository,
                                                    database_session=database_session)

    post_service: Factory["PostServiceI"] = Factory(PostService,
                                                        repository_post=post_repository,
                                                        repository_user=user_repository,
                                                        database_session=database_session)

container = DependencyContainer()