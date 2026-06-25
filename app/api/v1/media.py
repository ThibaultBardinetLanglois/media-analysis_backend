from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.media import MediaRead
from app.services.media_service import MediaService

router = APIRouter(prefix="/media")


@router.post("/upload", response_model=MediaRead, status_code=201)
def upload_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a media file and create its database record."""
    media_service = MediaService(db)

    return media_service.upload_media(file)


@router.get("", response_model=list[MediaRead])
def list_media(db: Session = Depends(get_db)):
    """List all uploaded media."""
    media_service = MediaService(db)

    return media_service.list_media()