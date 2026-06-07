from jose import jwt
from datetime import datetime
from datetime import timedelta

from config import *

def create_access_token(data):

    to_encode = data.copy()

    expire = (
        datetime.utcnow()
        +
        timedelta(
            minutes=
            ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {"exp": expire}
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def decode_token(token):

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload