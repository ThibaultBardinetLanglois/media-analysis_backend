from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    UPLOAD_SUBDIRECTORIES_BY_MEDIA_TYPE,
    build_safe_stored_filename,
    detect_real_mime_type,
    resolve_media_type,
    sanitize_original_filename,
)
from app.models.media import Media, MediaType
from app.repositories.media_repository import MediaRepository
from app.services.antivirus_service import AntivirusService


class MediaService:
    """
    Service responsible for media upload and storage.
    """

    def __init__(self, db: Session):
        """Initialize media service dependencies."""
        self.media_repository = MediaRepository(db)
        self.antivirus_service = AntivirusService()

    def list_media(self) -> list[Media]:
        """
        Return all uploaded media.
        """
        return self.media_repository.list_all()

    def upload_media(self, file: UploadFile) -> Media:
        """
        Upload, validate, scan and persist a media file.

        Processing pipeline:

        1. Validate that a filename has been provided.
        2. Sanitize the original filename to prevent path traversal attacks.
        3. Generate a unique storage filename (UUID) to avoid collisions.
        4. Save the uploaded file into a temporary directory while enforcing
        an absolute raw upload size limit.
        5. Detect the real MIME type using libmagic instead of trusting the
        MIME type declared by the client.
        6. Validate that the detected MIME type is consistent with the file
        extension and that both are supported.
        7. Validate the file size against the media-type-specific limit.
        8. Scan the uploaded file with the antivirus service.
        9. Move the validated file into its final storage directory according
        to its media type (documents, images, audio or video).
        10. Persist the media metadata into the database.
        11. Return the created media entity.
        """

        # ------------------------------------------------------------------
        # Step 1 - Validate filename
        # ------------------------------------------------------------------
        if not file.filename:
            raise HTTPException(status_code=400, detail="Missing filename")

        # ------------------------------------------------------------------
        # Step 2 - Sanitize filename
        # ------------------------------------------------------------------
        try:
            safe_original_filename = sanitize_original_filename(file.filename)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        # ------------------------------------------------------------------
        # Step 3 - Generate storage filename
        # ------------------------------------------------------------------
        stored_filename = build_safe_stored_filename(safe_original_filename)

        # ------------------------------------------------------------------
        # Step 4 - Save into temporary directory
        # ------------------------------------------------------------------
        base_upload_dir = Path(settings.UPLOAD_DIR)
        tmp_dir = base_upload_dir / "tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)

        tmp_file_path = tmp_dir / stored_filename

        size_bytes = self._save_file_with_raw_size_limit(
            file=file,
            file_path=tmp_file_path,
        )

        # ------------------------------------------------------------------
        # Step 5 - Detect the real MIME type
        # ------------------------------------------------------------------
        real_mime_type = detect_real_mime_type(str(tmp_file_path))

        # ------------------------------------------------------------------
        # Step 6 - Validate MIME type and extension
        # ------------------------------------------------------------------
        try:
            media_type = resolve_media_type(
                mime_type=real_mime_type,
                filename=safe_original_filename,
            )
        except ValueError as exc:
            tmp_file_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        # ------------------------------------------------------------------
        # Step 7 - Validate media-type-specific size
        # ------------------------------------------------------------------
        try:
            self._validate_size_for_media_type(
                size_bytes=size_bytes,
                media_type=media_type,
            )
        except HTTPException:
            tmp_file_path.unlink(missing_ok=True)
            raise

        # ------------------------------------------------------------------
        # Step 8 - Antivirus scan
        # ------------------------------------------------------------------
        if not self.antivirus_service.scan_file(tmp_file_path):
            tmp_file_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=400,
                detail="File rejected by antivirus scan",
            )

        # ------------------------------------------------------------------
        # Step 9 - Move into final storage
        # ------------------------------------------------------------------
        final_subdirectory = UPLOAD_SUBDIRECTORIES_BY_MEDIA_TYPE[media_type]
        final_dir = base_upload_dir / final_subdirectory
        final_dir.mkdir(parents=True, exist_ok=True)

        final_file_path = final_dir / stored_filename
        tmp_file_path.replace(final_file_path)

        # ------------------------------------------------------------------
        # Step 10 - Persist metadata
        # ------------------------------------------------------------------
        return self.media_repository.create(
            original_filename=safe_original_filename,
            stored_filename=stored_filename,
            file_path=str(final_file_path),
            mime_type=real_mime_type,
            media_type=MediaType(media_type),
            size_bytes=size_bytes,
        )

    def _save_file_with_raw_size_limit(
        self,
        file: UploadFile,
        file_path: Path,
    ) -> int:
        """
        Save file while enforcing the absolute raw upload size limit.
        """

        size_bytes = 0

        try:
            with file_path.open("wb") as buffer:
                while chunk := file.file.read(1024 * 1024):
                    size_bytes += len(chunk)

                    if size_bytes > settings.MAX_RAW_UPLOAD_SIZE_BYTES:
                        file_path.unlink(missing_ok=True)
                        raise HTTPException(
                            status_code=413,
                            detail=(
                                f"File too large. "
                                f"Max raw size is "
                                f"{settings.MAX_RAW_UPLOAD_SIZE_MB} MB"
                            ),
                        )

                    buffer.write(chunk)

        finally:
            file.file.close()

        return size_bytes

    def _validate_size_for_media_type(
        self,
        *,
        size_bytes: int,
        media_type: str,
    ) -> None:
        """
        Validate file size against the configured media-type-specific limit.
        """

        max_size_bytes = settings.MAX_UPLOAD_SIZE_BYTES_BY_MEDIA_TYPE[
            media_type
        ]

        if size_bytes > max_size_bytes:
            max_size_mb = max_size_bytes // (1024 * 1024)

            raise HTTPException(
                status_code=413,
                detail=(
                    f"File too large for {media_type}. "
                    f"Max size is {max_size_mb} MB"
                ),
            )