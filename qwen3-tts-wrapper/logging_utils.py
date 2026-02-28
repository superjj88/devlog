# logging_utils.py - Security-relevant logging utilities
import logging
import os
from pathlib import Path
from typing import Optional
from datetime import datetime
import json


class SecurityLogger:
    """
    Logger with security-focused features including:
    - Structured JSON logging
    - Sensitive data redaction
    - Security event tracking
    """

    # Patterns for sensitive data
    SENSITIVE_PATTERNS = [
        r"password\s*[=:]\s*\S+",
        r"api[_-]?key\s*[=:]\s*\S+",
        r"secret\s*[=:]\s*\S+",
        r"token\s*[=:]\s*\S+",
    ]

    def __init__(
        self,
        name: str = "qwen3tts",
        log_file: Optional[str] = None,
        level: int = logging.INFO,
    ):
        """
        Initialize the security logger.

        Args:
            name: Logger name
            log_file: Optional file path for logging
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Remove existing handlers
        self.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_format = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_format = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)

        # Security event counter
        self.security_events = []

    def redact_sensitive_data(self, message: str) -> str:
        """
        Redact sensitive data from log messages.

        Args:
            message: Original message

        Returns:
            Redacted message
        """
        import re

        # Redact common patterns
        patterns = [
            (r"password\s*[=:]\s*\S+", "password=***"),
            (r"api[_-]?key\s*[=:]\s*\S+", "api_key=***"),
            (r"secret\s*[=:]\s*\S+", "secret=***"),
            (r"token\s*[=:]\s*\S+", "token=***"),
        ]

        redacted = message
        for pattern, replacement in patterns:
            redacted = re.sub(pattern, replacement, redacted, flags=re.IGNORECASE)

        return redacted

    def log_security_event(
        self, event_type: str, details: dict, severity: str = "info"
    ):
        """
        Log a security event with structured data.

        Args:
            event_type: Type of security event
            details: Event details dictionary
            severity: Event severity (info, warning, error)
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "severity": severity,
            "details": details,
        }

        self.security_events.append(event)

        # Log with appropriate level
        if severity == "error":
            self.logger.error(f"[SECURITY] {event_type}: {json.dumps(details)}")
        elif severity == "warning":
            self.logger.warning(f"[SECURITY] {event_type}: {json.dumps(details)}")
        else:
            self.logger.info(f"[SECURITY] {event_type}: {json.dumps(details)}")

    def log_input_validation(
        self, input_type: str, is_valid: bool, error_msg: Optional[str] = None
    ):
        """
        Log input validation results.

        Args:
            input_type: Type of input validated
            is_valid: Whether validation passed
            error_msg: Error message if validation failed
        """
        details = {"input_type": input_type, "is_valid": is_valid}

        if error_msg:
            details["error_message"] = self.redact_sensitive_data(error_msg)

        if is_valid:
            self.logger.info(f"[VALIDATION] {input_type} passed validation")
        else:
            self.log_security_event(
                "input_validation_failed", details, severity="warning"
            )

    def log_rate_limit_event(self, client_id: str, is_allowed: bool, remaining: int):
        """
        Log rate limiting events.

        Args:
            client_id: Client identifier
            is_allowed: Whether request was allowed
            remaining: Remaining requests
        """
        details = {
            "client_id": client_id,
            "is_allowed": is_allowed,
            "remaining_requests": remaining,
        }

        if is_allowed:
            self.logger.info(
                f"[RATE_LIMIT] {client_id}: allowed ({remaining} remaining)"
            )
        else:
            self.log_security_event("rate_limit_exceeded", details, severity="warning")

    def log_command_execution(
        self, command: str, success: bool, error_msg: Optional[str] = None
    ):
        """
        Log command execution results.

        Args:
            command: Command executed
            success: Whether execution succeeded
            error_msg: Error message if failed
        """
        details = {"command": self.redact_sensitive_data(command), "success": success}

        if error_msg:
            details["error_message"] = self.redact_sensitive_data(error_msg)

        if success:
            self.logger.info(f"[COMMAND] Executed: {command}")
        else:
            self.log_security_event(
                "command_execution_failed", details, severity="error"
            )

    def log_file_operation(
        self,
        operation: str,
        file_path: str,
        success: bool,
        error_msg: Optional[str] = None,
    ):
        """
        Log file operation results.

        Args:
            operation: Type of file operation
            file_path: Path to file
            success: Whether operation succeeded
            error_msg: Error message if failed
        """
        details = {"operation": operation, "file_path": file_path, "success": success}

        if error_msg:
            details["error_message"] = error_msg

        if success:
            self.logger.info(f"[FILE] {operation}: {file_path}")
        else:
            self.log_security_event("file_operation_failed", details, severity="error")

    def get_security_events(self) -> list:
        """Get all logged security events."""
        return self.security_events

    def clear_security_events(self):
        """Clear all logged security events."""
        self.security_events.clear()


# Global logger instance
security_logger = SecurityLogger()


def log_security_event(event_type: str, details: dict, severity: str = "info"):
    """Log a security event using the global logger."""
    security_logger.log_security_event(event_type, details, severity)


def log_input_validation(
    input_type: str, is_valid: bool, error_msg: Optional[str] = None
):
    """Log input validation using the global logger."""
    security_logger.log_input_validation(input_type, is_valid, error_msg)


def log_rate_limit_event(client_id: str, is_allowed: bool, remaining: int):
    """Log rate limiting event using the global logger."""
    security_logger.log_rate_limit_event(client_id, is_allowed, remaining)


def log_command_execution(command: str, success: bool, error_msg: Optional[str] = None):
    """Log command execution using the global logger."""
    security_logger.log_command_execution(command, success, error_msg)


def log_file_operation(
    operation: str, file_path: str, success: bool, error_msg: Optional[str] = None
):
    """Log file operation using the global logger."""
    security_logger.log_file_operation(operation, file_path, success, error_msg)
