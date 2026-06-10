import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.media import MediaStatus, MediaType


class MediaBase(BaseModel):
    original_filename: str
    mime_type: str
    media_type: MediaType
    status: MediaStatus
    size_bytes: int | None = None


class MediaRead(MediaBase):
    id: uuid.UUID
    stored_filename: str
    file_path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True