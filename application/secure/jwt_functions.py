import jwt
import time

from api.api_v1.base_schemas.schemas import StandartException
from core.config import settings
from core.redis_db.redis_helper import redis_client


def validation(token: str):
    jwt_info = JwtInfo(token)
    if jwt_info.valid:
        return jwt_info
    else:
        raise StandartException(status_code=401, detail=jwt_info.info_except)


def create_jwt(user_id: int):
    payload = {
        "id": user_id,
        "expires": time.time() + 3600,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm='HS256')
    if redis_client.exists(user_id):
        redis_client.delete(user_id)
    redis_client.setex(user_id, 3600, "valid")
    return token

class JwtInfo:
    def __init__(self, token: str):
        self.valid = False
        try:
            data = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            self._expires = data.get("expires")
            self.id = data.get("id")
            self._jti=data.get("jti")
            self._verify_jwt()
            self.redis_client = redis_client
        except Exception as e:
            self.id = None
            self.info_except = str(e)

    def _verify_jwt(self):
        if self._expires is None:
            self.info_except = "data expire is none"
        elif time.time() > self._expires:
            self.info_except = "expired"
        elif not redis_client.exists(self.id):
            self.info_except = "Token revoked"
        else:
            self.valid = True
            self.info_except = None

    def logout(self):
        redis_client.delete(self.id)