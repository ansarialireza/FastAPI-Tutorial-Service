from app.core.config import settings
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError


class TokenManager:
    def __init__(self):
        self.secret_ky = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret_ky, algorithm=self.algorithm)

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = data.copy()
        to_encode.update({"type": "refresh"})
        return self.create_access_token(to_encode, expires_delta)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(
                token, self.secret_ky, algorithms=[self.algorithm]
            )
            return payload
        except JWTError:
            return None

    def get_username_from_token(self, token: str) -> Optional[str]:
        payload = self.verify_token(token)
        return payload.get("sub") if payload else None

    def get_token_type(self, token) -> Optional[str]:
        payload = self.verify_token(token)
        return payload.get("type") if payload else None
