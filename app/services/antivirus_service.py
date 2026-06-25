from pathlib import Path


class AntivirusService:
    """Service responsible for scanning uploaded files.

    For the POC, this service is intentionally implemented as a safe placeholder.
    In a production-like setup, this could call ClamAV, an internal scanner,
    or a sandboxed malware analysis service.
    """

    def scan_file(self, file_path: Path) -> bool:
        """Scan a file and return True when it is considered safe.

        Args:
            file_path: Path of the uploaded file to scan.

        Returns:
            True if the file passes the scan.
        """
        return file_path.exists()