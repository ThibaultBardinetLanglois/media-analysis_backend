from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    API_V1_PREFIX: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    UPLOAD_DIR: str
    MAX_RAW_UPLOAD_SIZE_MB: int
    MAX_TEXT_UPLOAD_SIZE_MB: int
    MAX_PDF_UPLOAD_SIZE_MB: int
    MAX_IMAGE_UPLOAD_SIZE_MB: int
    MAX_AUDIO_UPLOAD_SIZE_MB: int
    MAX_VIDEO_UPLOAD_SIZE_MB: int
    
    BACKEND_CORS_ORIGINS: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_LIFETIME: int

    COOKIE_SECURE: bool
    COOKIE_SAMESITE: str
    COOKIE_REFRESH_MAX_AGE: int
    
    @property
    def DATABASE_URL(self) -> str:
        """Build the SQLAlchemy-compatible PostgreSQL connection URL."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        
    @property
    def MAX_RAW_UPLOAD_SIZE_BYTES(self) -> int:
        """Return absolute max upload size in bytes."""
        return self.MAX_RAW_UPLOAD_SIZE_MB * 1024 * 1024
    
    @property
    def MAX_UPLOAD_SIZE_BYTES_BY_MEDIA_TYPE(self) -> dict[str, int]:
        """Return max upload size in bytes by media type."""
        return {
            "text": self.MAX_TEXT_UPLOAD_SIZE_MB * 1024 * 1024,
            "pdf": self.MAX_PDF_UPLOAD_SIZE_MB * 1024 * 1024,
            "image": self.MAX_IMAGE_UPLOAD_SIZE_MB * 1024 * 1024,
            "audio": self.MAX_AUDIO_UPLOAD_SIZE_MB * 1024 * 1024,
            "video": self.MAX_VIDEO_UPLOAD_SIZE_MB * 1024 * 1024,
        }
    
    class Config:
        env_file = ".env"
        case_sensitive = True

        
        
settings = Settings()