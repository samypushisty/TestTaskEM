import jwt
import time

from api.api_v1.base_schemas.schemas import StandartException
from core.config import settings


def validation(token: str):
    jwt_info = JwtInfo(token)
    if jwt_info.valid:
        return jwt_info
    else:
        raise StandartException(status_code=401, detail=jwt_info.info_except)


def create_jwt(chat_id: int):
    return jwt.encode(payload={'id': chat_id, "expires": time.time() + 3600},
                      key=settings.secret_key, algorithm='HS256')


class JwtInfo:
    def __init__(self, token: str):
        self.valid = False
        try:
            data = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            self._expires = data.get("expires")
            self.id = data.get("id")
            self._verify_jwt()
        except:
            self.id = None
            self.info_except = "invalid token or you haven't token"

    def _verify_jwt(self):
        if self._expires is None:
            self.info_except = "data expire is none"
        elif time.time() > self._expires:
            self.info_except = "expired"
        else:
            self.valid = True
            self.info_except = None