from typing import Dict, Optional, Tuple, Any
from sqlalchemy.orm import Session
from .password import PasswordManager
from .jwt import TokenManager
from app.crud.user import UserCRUD
from app.core.config import settings


class AuthService:
    def __init__(self):
        self.password_manager = PasswordManager()
        self.token_manager = TokenManager()

    def authenticate_user(
        self, db: Session, username: str, password: str, user_crud: UserCRUD
    ) -> Tuple[bool, Optional[Any]]:
        user = user_crud.get_by_username(username)
        if user is None:
            return False, None
        if not self.password_manager.verify_password(
            password, user.hashed_password
        ):
            return False, None
        return True, user

    def generate_tokens(self, username: str) -> Dict[str, str]:
        access_token = self.token_manager.create_access_token(
            data={"sub": username}
        )
        refresh_token = self.token_manager.create_refresh_token(
            data={"sub": username}
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        payload = self.token_manager.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        username = payload.get("sub")
        if not username:
            return None
        return self.token_manager.create_access_token(data={"sub": username})
