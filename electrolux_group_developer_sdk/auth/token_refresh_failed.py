class TokenRefreshFailedException(Exception):
    """Exception raised when an token is refreshed and an error is encountered."""

    def __init__(self, message: str = "Refreshing the token failed."):
        super().__init__(message)