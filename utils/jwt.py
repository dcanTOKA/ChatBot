import jwt
import datetime
from typing import Optional


class JWTUtils:
    SECRET_KEY = "PuzzleFasillari!"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWTUtils.SECRET_KEY, algorithm=JWTUtils.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, credentials_exception):
        try:
            payload = jwt.decode(token, JWTUtils.SECRET_KEY, algorithms=[JWTUtils.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            return username
        except jwt.PyJWTError:
            raise credentials_exception
