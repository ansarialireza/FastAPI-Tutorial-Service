from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, Any
from app.db.session import get_db
from app.crud.user import UserCRUD
from concurrent.interpreters import get_current
from .jwt import TokenManager

security = HTTPBearer()


class AuthDependencies:
    def __init__(self):
        self.token_manager = TokenManager()

    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
    ) -> Any:
        token = credentials.credentials
        username = self.token_manager.get_username_from_token(token)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        user = UserCRUD(db).get_by_username(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user

    async def get_current_active_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
    ):
        user = await self.get_current_user(credentials, db)
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )
        return user


auth_deps = AuthDependencies()
get_current_user = auth_deps.get_current_user
get_current_active_user = auth_deps.get_current_active_user
