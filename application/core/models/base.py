from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy import ForeignKey, text, String, MetaData, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from core.config import settings
import enum

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

class UserSettings(Base):
    __tablename__ = "settings"

    user_id: Mapped[intfkpk]
    theme: Mapped[Theme]
    language: Mapped[Language]
    notifications: Mapped[bool]

    class Config:
        use_enum_values = True
