class AuthData:
    def __init__(self, access_token: str, refresh_token: str, api_key: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.api_key = api_key
