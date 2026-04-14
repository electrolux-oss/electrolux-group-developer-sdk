from typing import Optional


class BadCredentialsException(Exception):
    """Exception raised when the credentials are missing or incorrect"""

    def __init__(self, message: str = "The credentials are incorrect.", status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
