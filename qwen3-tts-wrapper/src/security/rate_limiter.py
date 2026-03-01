# rate_limiter.py - Rate limiting mechanism to prevent abuse
import time
from collections import defaultdict
from threading import Lock
from typing import Dict, Optional, Tuple


class RateLimiter:
    """
    Thread-safe rate limiter using sliding window algorithm.
    """

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = Lock()

    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        """
        Check if a request is allowed for the given client.

        Args:
            client_id: Unique identifier for the client

        Returns:
            Tuple of (is_allowed, remaining_requests)
        """
        current_time = time.time()

        with self.lock:
            # Clean up old requests outside the window
            cutoff_time = current_time - self.window_seconds
            self.requests[client_id] = [
                t for t in self.requests[client_id] if t > cutoff_time
            ]

            # Check if under limit
            if len(self.requests[client_id]) >= self.max_requests:
                return False, 0

            # Record this request
            self.requests[client_id].append(current_time)

            # Calculate remaining requests
            remaining = self.max_requests - len(self.requests[client_id])

            return True, max(0, remaining)

    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for a client."""
        current_time = time.time()

        with self.lock:
            cutoff_time = current_time - self.window_seconds
            valid_requests = [t for t in self.requests[client_id] if t > cutoff_time]
            return max(0, self.max_requests - len(valid_requests))

    def reset(self, client_id: str) -> None:
        """Reset rate limit for a specific client."""
        with self.lock:
            self.requests[client_id] = []

    def reset_all(self) -> None:
        """Reset all rate limits."""
        with self.lock:
            self.requests.clear()


# Global rate limiter instance
rate_limiter = RateLimiter(
    max_requests=60,  # 60 requests per minute by default
    window_seconds=60,
)


def check_rate_limit(client_id: str) -> Tuple[bool, int, Optional[str]]:
    """
    Check rate limit and return result with optional error message.

    Args:
        client_id: Unique identifier for the client

    Returns:
        Tuple of (is_allowed, remaining, error_message)
    """
    is_allowed, remaining = rate_limiter.is_allowed(client_id)

    if not is_allowed:
        return False, 0, "Rate limit exceeded. Please try again later."

    return True, remaining, None


def get_rate_limit_headers(remaining: int) -> Dict[str, str]:
    """
    Get rate limit headers for response.

    Args:
        remaining: Remaining requests in current window

    Returns:
        Dictionary of rate limit headers
    """
    return {
        "X-RateLimit-Remaining": str(remaining),
        "X-RateLimit-Limit": str(rate_limiter.max_requests),
        "X-RateLimit-Window": str(rate_limiter.window_seconds),
    }
