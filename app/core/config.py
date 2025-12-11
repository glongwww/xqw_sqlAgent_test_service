from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tianji SQL Test Service"
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./sql_app.db"

    class Config:
        case_sensitive = True

settings = Settings()
