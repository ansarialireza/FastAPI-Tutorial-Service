from passlib.context import CryptContext
from typing import Optional
from core.config import settings


class PasswordManager:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=[settings.ALGORITHM], deprecated="auto"
        )

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def validate_password_policy(
        self, password: str
    ) -> tuple[bool, Optional[str]]:
        if len(password) < 8:
            return False, "Password must be least 8 characters long"
        return True, None
