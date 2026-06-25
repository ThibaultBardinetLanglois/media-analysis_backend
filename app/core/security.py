from pathlib import Path
from uuid import uuid4
import magic


ALLOWED_EXTENSIONS_BY_MEDIA_TYPE = {
    "text": {".txt"},
    "pdf": {".pdf"},
    "image": {".jpg", ".jpeg", ".png"},
    "audio": {".mp3", ".wav", ".m4a"},
    "video": {".mp4", ".mov", ".mkv"},
}

ALLOWED_MIME_TYPES = {
    "text/plain": "text",
    "application/pdf": "pdf",
    "image/jpeg": "image",
    "image/png": "image",
    "audio/mpeg": "audio",
    "audio/wav": "audio",
    "audio/x-wav": "audio",
    "audio/mp4": "audio",
    "video/mp4": "video",
    "video/quicktime": "video",
    "video/x-matroska": "video",
}

UPLOAD_SUBDIRECTORIES_BY_MEDIA_TYPE = {
    "text": "documents",
    "pdf": "documents",
    "image": "images",
    "audio": "audio",
    "video": "video",
}


def sanitize_original_filename(filename: str) -> str:
    if filename != Path(filename).name:
        raise ValueError("Invalid filename")

    return filename


def get_file_extension(filename: str) -> str:
    """Extract and normalize the file extension."""
    return Path(filename).suffix.lower()


def resolve_media_type(mime_type: str, filename: str) -> str:
    """Resolve media type from MIME type and extension.

    Raises:
        ValueError: If MIME type or extension is not allowed.
    """
    media_type = ALLOWED_MIME_TYPES.get(mime_type)

    if media_type is None:
        raise ValueError("Unsupported MIME type")

    extension = get_file_extension(filename)
    allowed_extensions = ALLOWED_EXTENSIONS_BY_MEDIA_TYPE[media_type]

    if extension not in allowed_extensions:
        raise ValueError("Unsupported file extension")

    return media_type


def build_safe_stored_filename(original_filename: str) -> str:
    """Generate a storage filename that prevents path traversal and collisions."""
    extension = get_file_extension(original_filename)

    return f"{uuid4()}{extension}"


def detect_real_mime_type(file_path: Path) -> str:
    """
    Detect actual MIME type using file content.
    """
    return magic.from_file(
        str(file_path),
        mime=True,
    )