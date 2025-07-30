import hashlib

from api.v1.base_schemas.schemas import StandartException

import sys
import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

def hash_password(password):
    logger.debug("Hash password")
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_password, provided_password):
    logger.debug("Check password")
    if not stored_password == hashlib.sha256(provided_password.encode()).hexdigest():
        logger.error("Invalid password")
        raise StandartException(status_code=401, detail="invalid password")
    logger.debug("Success")