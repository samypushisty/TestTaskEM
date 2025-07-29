from typing import Optional
from pydantic import BaseModel, field_validator
from core.models.base import Theme, Language


class UserSettingsPatch(BaseModel):
    theme: Optional[Theme] = None
    language: Optional[Language] = None
    notifications: Optional[bool] = None

    class Config:
        use_enum_values = True


class UserSettingsRead(BaseModel):
    user_id: int
    theme: Theme
    language: Language
    notifications: bool

    class Config:
        validate_assignment = True
        use_enum_values = True

    @field_validator('language', mode='before')
    def validate_language(cls, value):
        if isinstance(value, Language):
            return Language(value).value
        return value


    @field_validator('theme', mode='before')
    def validate_theme(cls, value):
        if isinstance(value, Theme):
            return Theme(value).value
        return value