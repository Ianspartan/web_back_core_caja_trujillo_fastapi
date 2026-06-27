from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # URL del backend del Core Financiero
    PORTAL_BACKEND_URL: str = "http://localhost:8000"

    # Puerto del Core
    PORT: int = 8001

    class Config:
        env_file = ".env"


settings = Settings()