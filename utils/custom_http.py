from typing import Optional

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
import jwt
from utils.jwt import JWTUtils


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        credentials = await super().__call__(request)
        if credentials:
            try:
                payload = jwt.decode(credentials.credentials, JWTUtils.SECRET_KEY, algorithms=[JWTUtils.ALGORITHM])
                return payload
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token is expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code")
