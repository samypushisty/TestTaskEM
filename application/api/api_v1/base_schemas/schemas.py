from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
T = TypeVar('T')


class GenericResponse(BaseModel, Generic[T]):
    status_code: int = 200
    detail: Optional[T] = None

class StandartException(Exception):
    def __init__(self, detail: str, status_code: int):
        self.status_code = status_code
        self.detail = {"status_code": status_code, "detail": detail}