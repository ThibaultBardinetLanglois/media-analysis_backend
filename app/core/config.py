from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_PREFIX: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    
    DATABASE_URL: str
    UPLOAD_DIR: str
    BACKEND_CORS_ORIGINS: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_LIFETIME: int

    COOKIE_SECURE: bool
    COOKIE_SAMESITE: str
    COOKIE_REFRESH_MAX_AGE: int
    
    class Config:
        env_file = ".env"
        
        
settings = Settings()