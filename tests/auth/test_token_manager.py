import time

import jwt
import pytest
from aioresponses import aioresponses

from electrolux_group_developer_sdk.auth.invalid_credentials_exception import InvalidCredentialsException
from electrolux_group_developer_sdk.auth.token_manager import TokenManager


def generate_token(exp_seconds_from_now):
    if exp_seconds_from_now is None:
        payload = {
            "sub": "test-user"
        }
    else:
        payload = {
            "exp": time.time() + exp_seconds_from_now,
            "sub": "test-user"
        }
    return jwt.encode(payload, "test-secret", algorithm="HS256")


ACCESS_TOKEN = generate_token(120)
NEW_ACCESS_TOKEN = generate_token(120)
EXPIRED_ACCESS_TOKEN = generate_token(-120)


class TestTokenManager():
    def test_update_success(self):
        token_manager = TokenManager(ACCESS_TOKEN, "mock_refresh_token", "mock_api_key")
        token_manager.update(NEW_ACCESS_TOKEN, "new_mock_refresh_token", "mock_api_key")
        assert token_manager._auth_data.access_token == NEW_ACCESS_TOKEN
        assert token_manager._auth_data.refresh_token == "new_mock_refresh_token"
        assert token_manager._auth_data.api_key == "mock_api_key"

    def test_get_user_id_success(self):
        token = generate_token(120)

        token_manager = TokenManager(token, "mock_refresh_token", "mock_api_key")

        user_id = token_manager.get_user_id()

        assert user_id == "test-user"

    def test_ensure_credentials_success(self):
        token_manager = TokenManager(ACCESS_TOKEN, "mock_refresh_token", "mock_api_key")
        try:
            token_manager.ensure_credentials()
        except Exception as e:
            pytest.fail(f"ensure_credentials() raised an exception: {e}")

    def test_ensure_credentials_api_key_missing(self):
        token_manager = TokenManager(ACCESS_TOKEN, "mock_refresh_token", None)
        with pytest.raises(InvalidCredentialsException):
            token_manager.ensure_credentials()

    def test_ensure_credentials_refresh_token_missing(self):
        token_manager = TokenManager(ACCESS_TOKEN, None, "mock_api_key")
        with pytest.raises(InvalidCredentialsException):
            token_manager.ensure_credentials()

    def test_is_token_valid_true(self):
        token = generate_token(120)
        manager = TokenManager(token, "refresh_token", "api_key")
        assert manager.is_token_valid() is True

    def test_is_token_valid_false(self):
        token = generate_token(-120)
        manager = TokenManager(token, "refresh_token", "api_key")
        assert manager.is_token_valid() is False

    def test_is_token_valid_missing_exp(self):
        token = generate_token(None)
        manager = TokenManager(token, "refresh_token", "api_key")
        assert manager.is_token_valid() is False

    @pytest.mark.asyncio
    async def test_refresh_token_success(self):

        token_manager = TokenManager(
            access_token=EXPIRED_ACCESS_TOKEN,
            refresh_token="mock_refresh_token",
            api_key="mock_api_key",
        )

        with aioresponses() as mocked:
            # Mock the response for the token refresh
            refresh_url = "https://api.developer.electrolux.one/api/v1/token/refresh"
            mocked.post(
                refresh_url,
                payload={
                    "accessToken": "new_access_token",
                    "refreshToken": "new_refresh_token",
                },
            )

            response = await token_manager.refresh_token()

            # Assertions
            assert response == True
            assert token_manager._auth_data.access_token == "new_access_token"
            assert token_manager._auth_data.refresh_token == "new_refresh_token"

    @pytest.mark.asyncio
    async def test_refresh_token_refresh_token_fails(self):
        token_manager = TokenManager(
            access_token=EXPIRED_ACCESS_TOKEN,
            refresh_token="mock_refresh_token",
            api_key="mock_api_key",
        )

        with aioresponses() as mocked:
            # Mock the response for the token refresh
            refresh_url = "https://api.developer.electrolux.one/api/v1/token/refresh"
            mocked.post(
                refresh_url,
                status=401
            )

            response = await token_manager.refresh_token()

            # Assertions
            assert response == False

    @pytest.mark.asyncio
    async def test_revoke_token_success(self):
        token_manager = TokenManager(
            access_token=ACCESS_TOKEN,
            refresh_token="mock_refresh_token",
            api_key="mock_api_key",
        )

        with aioresponses() as mocked:
            # Mock the response for the token revoke
            refresh_url = "https://api.developer.electrolux.one/api/v1/token/revoke"
            mocked.post(
                refresh_url,
                payload={},
            )

            response = await token_manager.revoke_token()

            # Assertions
            assert response == True
            assert token_manager._auth_data is None

    @pytest.mark.asyncio
    async def test_revoke_token_revoke_token_fails(self):
        token_manager = TokenManager(
            access_token=EXPIRED_ACCESS_TOKEN,
            refresh_token="mock_refresh_token",
            api_key="mock_api_key",
        )

        with aioresponses() as mocked:
            # Mock the response for the token revoke
            refresh_url = "https://api.developer.electrolux.one/api/v1/token/revoke"
            mocked.post(
                refresh_url,
                status=401
            )

            response = await token_manager.revoke_token()

            # Assertions
            assert response == False

    @pytest.mark.asyncio
    async def test_get_auth_data_success(self):
        token = generate_token(120)

        token_manager = TokenManager(
            access_token=token,
            refresh_token="mock_refresh_token",
            api_key="mock_api_key",
        )

        response = await token_manager.get_auth_data()

        # Assertions
        assert response.access_token == token
        assert response.refresh_token == "mock_refresh_token"
        assert response.api_key == "mock_api_key"

    @pytest.mark.asyncio
    async def test_get_auth_data_token_expired_success(self):
        token = generate_token(-120)

        token_manager = TokenManager(
            access_token=token,
            refresh_token="mock_refresh_token",
            api_key="mock_api_key",
        )

        with aioresponses() as mocked:
            refresh_url = "https://api.developer.electrolux.one/api/v1/token/refresh"

            # Mock the response for the token refresh
            mocked.post(
                refresh_url,
                status=200,
                payload={
                    "accessToken": "new_access_token",
                    "refreshToken": "new_refresh_token",
                },
            )

            response = await token_manager.get_auth_data()

            # Assertions
            assert response.access_token == "new_access_token"
            assert response.refresh_token == "new_refresh_token"
            assert response.api_key == "mock_api_key"

    @pytest.mark.asyncio
    async def test_get_auth_data_refresh_token_fails(self):
        token = generate_token(-120)
        token_manager = TokenManager(
            access_token=token,
            refresh_token="mock_refresh_token",
            api_key="mock_api_key",
        )

        with aioresponses() as mocked:
            refresh_url = "https://api.developer.electrolux.one/api/v1/token/refresh"

            # Mock the response for the token refresh
            mocked.post(
                refresh_url,
                status=401
            )

            with pytest.raises(Exception):
                await token_manager.get_auth_data()
