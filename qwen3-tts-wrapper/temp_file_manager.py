# temp_file_manager.py - Secure temporary file handling with cleanup
import os
import tempfile
import stat
from pathlib import Path
from typing import Optional, List
import atexit


class TempFileManager:
    """
    Manages temporary files with secure permissions and automatic cleanup.
    """

    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the temporary file manager.

        Args:
            base_dir: Base directory for temporary files (defaults to system temp)
        """
        self.base_dir = Path(base_dir) if base_dir else Path(tempfile.gettempdir())
        self.created_files: List[Path] = []
        self.locked_files: set = set()

        # Register cleanup on exit
        atexit.register(self.cleanup)

    def create_secure_file(self, prefix: str = "qwen_", suffix: str = ".wav") -> Path:
        """
        Create a temporary file with secure permissions.

        Args:
            prefix: Filename prefix
            suffix: Filename suffix

        Returns:
            Path to the created file
        """
        # Create directory if it doesn't exist
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Create secure temporary file
        fd, path = tempfile.mkstemp(
            prefix=prefix, suffix=suffix, dir=str(self.base_dir)
        )

        # Close the file descriptor immediately
        os.close(fd)

        # Set secure permissions (owner read/write only)
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)

        # Track the file
        file_path = Path(path)
        self.created_files.append(file_path)
        self.locked_files.add(file_path)

        return file_path

    def create_secure_temp_dir(self, prefix: str = "qwen_") -> Path:
        """
        Create a temporary directory with secure permissions.

        Args:
            prefix: Directory name prefix

        Returns:
            Path to the created directory
        """
        # Create directory if it doesn't exist
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Create secure temporary directory
        dir_path = tempfile.mkdtemp(prefix=prefix, dir=str(self.base_dir))

        # Set secure permissions (owner read/write/execute)
        os.chmod(dir_path, stat.S_IRWXU)

        return Path(dir_path)

    def cleanup_file(self, file_path: Path) -> bool:
        """
        Safely delete a specific file.

        Args:
            file_path: Path to the file to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            if file_path.exists() and file_path.is_file():
                # Remove write permission before deleting
                file_path.chmod(stat.S_IRUSR)
                file_path.unlink()

                # Remove from tracking
                if file_path in self.created_files:
                    self.created_files.remove(file_path)
                if file_path in self.locked_files:
                    self.locked_files.remove(file_path)

                return True
        except Exception as e:
            print(f"[TempFileManager] Error deleting file {file_path}: {e}")
            return False

        return False

    def cleanup(self) -> None:
        """
        Clean up all tracked temporary files.
        """
        for file_path in list(self.created_files):
            self.cleanup_file(file_path)

        self.created_files.clear()
        self.locked_files.clear()

    def cleanup_old_files(self, max_age_seconds: int = 3600) -> int:
        """
        Clean up files older than max_age_seconds.

        Args:
            max_age_seconds: Maximum age in seconds

        Returns:
            Number of files cleaned up
        """
        cleaned = 0
        current_time = os.path.getmtime

        for file_path in list(self.created_files):
            try:
                mtime = os.path.getmtime(str(file_path))
                age = current_time(file_path) - mtime

                if age > max_age_seconds:
                    if self.cleanup_file(file_path):
                        cleaned += 1
            except Exception:
                continue

        return cleaned

    def get_created_files(self) -> List[Path]:
        """Get list of all tracked temporary files."""
        return list(self.created_files)

    def is_locked(self, file_path: Path) -> bool:
        """Check if a file is locked (in use)."""
        return file_path in self.locked_files

    def unlock(self, file_path: Path) -> None:
        """Unlock a file for cleanup."""
        if file_path in self.locked_files:
            self.locked_files.remove(file_path)


# Global instance
temp_manager = TempFileManager()


def create_secure_temp_file(prefix: str = "qwen_", suffix: str = ".wav") -> Path:
    """Create a secure temporary file using the global manager."""
    return temp_manager.create_secure_file(prefix, suffix)


def cleanup_temp_files() -> None:
    """Cleanup all temporary files using the global manager."""
    temp_manager.cleanup()


def cleanup_old_temp_files(max_age_seconds: int = 3600) -> int:
    """Cleanup old temporary files using the global manager."""
    return temp_manager.cleanup_old_files(max_age_seconds)
