from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Cost Manager"
    DATABASE_URL: str = "sqlite:///./database.db"

    # JWT settings
    JWT_SECRET_KEY: str = "AERHGAr;oihaegrAERHg;n'ihihsldkvojdsafAERHkaerhioa"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Password hashing settings
    PASSWORD_HASH_SCHEME: str = "pbkdf2_sha256"  # bcrypt, argon2, sha256_crypt

    FIRST_SUPERUSER: str = "admin@admin.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"

    class Config:
        env_file = ".env"


settings = Settings()
