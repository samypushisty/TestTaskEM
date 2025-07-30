from datetime import datetime
from typing import Annotated, Optional, List
from sqlalchemy import ForeignKey, text, String, MetaData, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from core.config import settings
import enum

import sys
import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

str_15 = Annotated[str,15]
str_256 = Annotated[str,256]
intfk = Annotated[int, mapped_column(BigInteger, ForeignKey("user.user_id", ondelete="CASCADE"))]
intfkpk = Annotated[int, mapped_column(BigInteger, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True)]
intpk = Annotated[int, mapped_column( primary_key=True, autoincrement=True)]


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )
    type_annotation_map = {
        str_15: String(15),
        str_256: String(256)
    }


class Language(enum.Enum):
    english = "english"
    russian = "russian"

class Theme(enum.Enum):
    black = "black"
    white = "white"
    auto = "auto"


class UserPermissionAssociation(Base):
    __tablename__ = 'user_permission_association'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete="CASCADE"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey('permission.permission_id', ondelete="CASCADE"), primary_key=True)



class Permission(Base):
    __tablename__ = "permission"

    permission_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]]

    users: Mapped[List["User"]] = relationship(
        secondary="user_permission_association",
        back_populates="permissions"
    )

class Post(Base):
    __tablename__ = "post"

    table_id: Mapped[intpk]
    user_id: Mapped[intfk]
    title: Mapped[str_15]
    description: Mapped[Optional[str_256]]

class User(Base):
    __tablename__ = "user"
    user_id: Mapped[intpk]
    password: Mapped[str]
    registration: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    last_visit: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str_15]
    last_name: Mapped[str_15]
    description: Mapped[Optional[str_256]]
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    permissions: Mapped[List["Permission"]] = relationship(
        secondary="user_permission_association",
        back_populates="users",
        lazy="selectin"  # Для автоматической загрузки при запросе
    )

    posts: Mapped[List["Post"]] = relationship(
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def has_permission(self, permission_name: str) -> bool:
        logger.debug("check Permission")
        logger.debug("Success")
        return any(p.name == permission_name for p in self.permissions)


class UserSettings(Base):
    __tablename__ = "settings"

    user_id: Mapped[intfkpk]
    theme: Mapped[Theme]
    language: Mapped[Language]
    notifications: Mapped[bool]

    class Config:
        use_enum_values = True
