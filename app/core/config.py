from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Cost Manager"
    DATABASE_URL: str = "sqlite:///./database.db"

    # JWT
    SECRET_KEY: str = "AERHGAr;oihaegrAERHg;ohiargjo'ijdsafAERHkaerhioa"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALGORITHM: str = "SHA-256"

    FIRST_SUPERUSER: str = "admin@admin.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"

    class Config:
        env_file = ".env"


settings = Settings()
