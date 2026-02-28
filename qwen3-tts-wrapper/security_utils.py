# security_utils.py - Security utilities for input validation and sanitization
import re
from typing import Tuple, Optional


# Maximum input length to prevent abuse
MAX_INPUT_LENGTH = 1000
MAX_RESPONSE_LENGTH = 5000

# Patterns for detecting potentially malicious input
MALICIOUS_PATTERNS = [
    r"<script[^>]*>.*?</script>",  # XSS attempts
    r"javascript:",  # JavaScript protocol
    r"on\w+\s*=",  # Event handlers
    r"<iframe[^>]*>",  # Iframe injection
    r"eval\s*\(",  # Eval attempts
    r"exec\s*\(",  # Exec attempts
    r"--",  # SQL comment
    r"\bUNION\b.*\bSELECT\b",  # SQL injection
    r"\bDROP\b.*\bTABLE\b",  # SQL injection
    r"\bINSERT\b.*\bINTO\b",  # SQL injection
    r"\bDELETE\b.*\bFROM\b",  # SQL injection
    r"\bUPDATE\b.*\bSET\b",  # SQL injection
    r"\bOR\b\s+\d+\s*=\s*\d+",  # SQL injection
    r"\bAND\b\s+\d+\s*=\s*\d+",  # SQL injection
]

# Allowed characters (basic Latin alphabet, numbers, punctuation, Hebrew)
ALLOWED_PATTERN = re.compile(
    r"^[\w\s\.\,\!\?\:\;\-\_\@\#\$\%\^\&\*\(\)\[\]\{\}\|\~\`\'\"\<\>\u0590-\u05FF]+$"
)


def sanitize_text(text: str) -> str:
    """
    Sanitize user input text by removing potentially malicious content.

    Args:
        text: Raw user input text

    Returns:
        Sanitized text safe for processing
    """
    if not isinstance(text, str):
        return ""

    # Truncate to maximum length
    text = text[:MAX_INPUT_LENGTH]

    # Remove null bytes and control characters (except newline, tab)
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]*>", "", text)

    # Remove JavaScript protocol
    text = re.sub(r"javascript:", "", text, flags=re.IGNORECASE)

    # Remove event handlers
    text = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', "", text, flags=re.IGNORECASE)

    # Remove eval/exec attempts
    text = re.sub(r"\b(eval|exec)\s*\(", "", text, flags=re.IGNORECASE)

    return text.strip()


def validate_text(text: str) -> Tuple[bool, Optional[str]]:
    """
    Validate user input text for security.

    Args:
        text: User input text to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not isinstance(text, str):
        return False, "Input must be a non-empty string"

    # Check length
    if len(text) > MAX_INPUT_LENGTH:
        return False, f"Input exceeds maximum length of {MAX_INPUT_LENGTH} characters"

    if len(text) < 2:
        return False, "Input is too short"

    # Check for malicious patterns
    for pattern in MALICIOUS_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return False, "Input contains potentially malicious content"

    # Check for allowed characters
    if not ALLOWED_PATTERN.match(text):
        return False, "Input contains invalid characters"

    return True, None


def validate_command(cmd: dict) -> Tuple[bool, Optional[str]]:
    """
    Validate command received via socket.

    Args:
        cmd: Command dictionary from socket

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(cmd, dict):
        return False, "Command must be a dictionary"

    # Check for required fields
    if "action" not in cmd:
        return False, "Command must contain 'action' field"

    # Validate action value
    valid_actions = ["start", "stop", "status"]
    if cmd["action"] not in valid_actions:
        return False, f"Invalid action. Must be one of: {', '.join(valid_actions)}"

    return True, None


def sanitize_response(response: str) -> str:
    """
    Sanitize response text before sending to TTS.

    Args:
        response: Response text to sanitize

    Returns:
        Sanitized response text
    """
    if not response or not isinstance(response, str):
        return ""

    # Truncate to maximum length
    response = response[:MAX_RESPONSE_LENGTH]

    # Remove null bytes and control characters
    response = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", response)

    return response.strip()
