from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Cost Manager"
    DATABASE_URL: str = "sqlite:///./database.db"
    SECRET_KEY: str = "AERHGAr;oihaegrAERHg;ohiargjo'ijdsafAERHkaerhioa"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    FIRST_SUPERUSER: str = "admin@admin.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"

    class Config:
        env_file = ".env"


settings = Settings()
