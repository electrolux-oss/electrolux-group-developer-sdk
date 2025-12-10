from typing import Optional


class FailedConnectionException(Exception):
    """Exception raised when connection fails"""

    def __init__(self, message: str = "The connection failed.", status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
