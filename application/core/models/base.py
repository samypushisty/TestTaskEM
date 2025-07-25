from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated, List
from sqlalchemy import ForeignKey, text, String, MetaData, BigInteger, Numeric, UniqueConstraint, ARRAY, event
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from core.config import settings
import enum

str_3 = Annotated[str,3]
str_15 = Annotated[str,15]
str_256 = Annotated[str,256]
intfk = Annotated[int, mapped_column(BigInteger, ForeignKey("user.chat_id", ondelete="CASCADE"))]
intfkpk = Annotated[int, mapped_column(BigInteger, ForeignKey("user.chat_id", ondelete="CASCADE"), primary_key=True)]
intpk = Annotated[int, mapped_column( primary_key=True, autoincrement=True)]


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )
    type_annotation_map = {
        str_3: String(3),
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
    chat_id: Mapped[int] = mapped_column( BigInteger, primary_key=True, autoincrement=False)
    password: Mapped[str]
    registration: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    last_visit: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

class UserSettings(Base):
    __tablename__ = "settings"

    chat_id: Mapped[intfkpk]
    theme: Mapped[Theme]
    language: Mapped[Language]
    notifications: Mapped[bool]

    class Config:
        use_enum_values = True
