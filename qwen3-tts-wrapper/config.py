# config.py - Configuration management with environment variables
import os
from pathlib import Path
from typing import Optional

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv not available, use system environment variables


def get_env_string(
    key: str, default: Optional[str] = None, required: bool = False
) -> Optional[str]:
    """Get a string environment variable."""
    value = os.getenv(key, default)
    if required and (value is None or value == ""):
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value


def get_env_int(key: str, default: int, required: bool = False) -> int:
    """Get an integer environment variable."""
    value = os.getenv(key)
    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return default
    try:
        return int(value)
    except ValueError:
        if required:
            raise ValueError(f"Environment variable '{key}' must be an integer")
        return default


def get_env_float(key: str, default: float, required: bool = False) -> float:
    """Get a float environment variable."""
    value = os.getenv(key)
    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return default
    try:
        return float(value)
    except ValueError:
        if required:
            raise ValueError(f"Environment variable '{key}' must be a float")
        return default


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get a boolean environment variable."""
    value = os.getenv(key, str(default)).lower()
    return value in ("true", "1", "yes", "on")


def get_env_path(
    key: str, default: Optional[str] = None, required: bool = False
) -> Path:
    """Get a path environment variable and return as Path object."""
    value = get_env_string(key, default, required)
    if value is None:
        return None
    return Path(value).expanduser().resolve()


# Model configuration
MODEL_DIR = get_env_string("MODEL_DIR", "/mnt/storage/models/qwen3-tts")
TTS_MODEL_PATH = get_env_string("TTS_MODEL_PATH", f"{MODEL_DIR}/1.7B-CustomVoice")

# Socket configuration
SOCKET_PATH = get_env_string("SOCKET_PATH", "/tmp/qwen3tts.sock")

# Temporary file configuration
TEMP_PLAY_FILE = get_env_string("TEMP_PLAY_FILE", "/tmp/qwen_play.wav")

# Audio processing thresholds
SILENCE_THRESHOLD = get_env_float("SILENCE_THRESHOLD", 0.02)
SILENCE_DURATION = get_env_float("SILENCE_DURATION", 2.5)

# Rate limiting configuration
RATE_LIMIT_REQUESTS = get_env_int("RATE_LIMIT_REQUESTS", 60)
RATE_LIMIT_WINDOW = get_env_int("RATE_LIMIT_WINDOW", 60)

# Logging configuration
LOG_LEVEL = get_env_string("LOG_LEVEL", "INFO")
LOG_FILE = get_env_string("LOG_FILE", "/var/log/qwen3tts.log")

# Socket permissions (octal string)
SOCKET_PERMISSIONS = get_env_string("SOCKET_PERMISSIONS", "0660")


def validate_config() -> list[str]:
    """Validate configuration and return list of warnings."""
    warnings = []

    # Check if MODEL_DIR exists
    if not Path(MODEL_DIR).exists():
        warnings.append(f"Model directory does not exist: {MODEL_DIR}")

    # Check if TTS_MODEL_PATH exists
    if not Path(TTS_MODEL_PATH).exists():
        warnings.append(f"TTS model path does not exist: {TTS_MODEL_PATH}")

    # Check socket path directory
    socket_path = Path(SOCKET_PATH)
    if not socket_path.parent.exists():
        warnings.append(f"Socket directory does not exist: {socket_path.parent}")

    return warnings


def get_config_summary() -> str:
    """Return a summary of the current configuration (without sensitive data)."""
    return f"""
Configuration Summary:
- MODEL_DIR: {MODEL_DIR}
- TTS_MODEL_PATH: {TTS_MODEL_PATH}
- SOCKET_PATH: {SOCKET_PATH}
- TEMP_PLAY_FILE: {TEMP_PLAY_FILE}
- SILENCE_THRESHOLD: {SILENCE_THRESHOLD}
- SILENCE_DURATION: {SILENCE_DURATION}
- RATE_LIMIT_REQUESTS: {RATE_LIMIT_REQUESTS}
- RATE_LIMIT_WINDOW: {RATE_LIMIT_WINDOW}
- LOG_LEVEL: {LOG_LEVEL}
- LOG_FILE: {LOG_FILE}
- SOCKET_PERMISSIONS: {SOCKET_PERMISSIONS}
"""
