from typing import Dict, Optional, Tuple
from sqlalchemy.orm import Session
from .password import PasswordManager
from .jwt import TokenManager
from app.core.config import settings


class AuthService:
    def __init__(self):
        self.password_manager = PasswordManager()
        self.token_manager = TokenManager()

    def authenticate_user(self):
        pass

    def generate_tokens(self):
        pass

    def refresh_access_token(self):
        pass
