class FailedConnectionException(Exception):
    """Exception raised when connection fails"""

    def __init__(self, message: str = "The connection failed."):
        super().__init__(message)