import bcrypt
import traceback
import jwt
from jwcrypto import jwk

from settings import path_private_key, path_public_key, algorithm, expire_minutes
from datetime import datetime, timedelta


def encode_jwt(
        payload: dict,
        private_key: str = path_private_key.read_text(),
        algorithm_: str = algorithm,
        expire_minutes_: int = expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes_)
    to_encode.update(
        iat=now,
        exp=expire,
    )

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm_,
    )

    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = path_public_key.read_text(),
        algorithm_: str = algorithm,
) -> dict:
    try:
        decoded = jwt.decode(
            str(token),
            str(public_key),
            algorithms=[algorithm_],
        )
    except Exception as exp:
        print(f"decode_jwt ERROR  {exp}")
        traceback.print_exc()
        raise
    return decoded


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)
