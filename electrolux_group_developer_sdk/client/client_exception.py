class ApplianceClientException(Exception):
    """Base exception for errors raised by the Appliance client."""

    def __init__(self, message: str = "An unknown error occurred in the Appiance client.", status: int | None = None):
        super().__init__(message)
        self.status = status