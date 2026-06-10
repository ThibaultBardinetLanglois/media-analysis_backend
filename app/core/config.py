from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_PREFIX: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    UPLOAD_DIR: str
    BACKEND_CORS_ORIGINS: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_LIFETIME: int

    COOKIE_SECURE: bool
    COOKIE_SAMESITE: str
    COOKIE_REFRESH_MAX_AGE: int
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = True

        
        
settings = Settings()