class InvalidTokenException(Exception):
    """Exception raised when an invalid token is encountered."""

    def __init__(self, message: str = "The token is invalid."):
        super().__init__(message)