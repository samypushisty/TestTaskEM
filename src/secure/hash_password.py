import hashlib

from api.v1.base_schemas.schemas import StandartException


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_password, provided_password):
    if not stored_password == hashlib.sha256(provided_password.encode()).hexdigest():
        raise StandartException(status_code=401, detail="invalid password")