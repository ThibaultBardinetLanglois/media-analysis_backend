from sqlalchemy.orm import Session

from app.models.media import Media, MediaStatus, MediaType


class MediaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        original_filename: str,
        stored_filename: str,
        file_path: str,
        mime_type: str,
        media_type: MediaType,
        size_bytes: int | None = None,
    ) -> Media:
        media = Media(
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_path=file_path,
            mime_type=mime_type,
            media_type=media_type,
            status=MediaStatus.PENDING,
            size_bytes=size_bytes,
        )

        self.db.add(media)
        self.db.commit()
        self.db.refresh(media)

        return media

    def list_all(self) -> list[Media]:
        return (
            self.db.query(Media)
            .order_by(Media.created_at.desc())
            .all()
        )