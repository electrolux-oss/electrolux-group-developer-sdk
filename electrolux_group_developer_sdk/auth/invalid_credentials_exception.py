class InvalidCredentialsException(Exception):
    """Exception raised for invalid credentials."""

    def __init__(self, message: str = "The credentials are invalid."):
        super().__init__(message)