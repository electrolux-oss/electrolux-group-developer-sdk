import asyncio
import time

import jwt
import pytest
from aioresponses import aioresponses
from yarl import URL

from electrolux_group_developer_sdk.auth.invalid_credentials_exception import InvalidCredentialsException
from electrolux_group_developer_sdk.auth.invalid_grant_exception import InvalidGrantException
from electrolux_group_developer_sdk.auth.invalid_token_exception import InvalidTokenException
from electrolux_group_developer_sdk.auth.token_manager import TokenManager, get_user_id_from_token
from electrolux_group_developer_sdk.auth.token_refresh_failed import TokenRefreshFailedException


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
    return jwt.encode(payload, "test-secret-at-least-32-bytes-long", algorithm="HS256")


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

    def test_init_does_not_trigger_on_token_update(self):
        callback_called = False

        def on_update(access_token, refresh_token, api_key):
            nonlocal callback_called
            callback_called = True

        token_manager = TokenManager(
            ACCESS_TOKEN,
            "mock_refresh_token",
            "mock_api_key",
            on_token_update=on_update,
        )
        assert callback_called is False

        token_manager.update(NEW_ACCESS_TOKEN, "new_refresh_token", "mock_api_key")
        assert callback_called is True

    def test_get_user_id_success(self):
        token = generate_token(120)

        token_manager = TokenManager(token, "mock_refresh_token", "mock_api_key")

        user_id = token_manager.get_user_id()

        assert user_id == "test-user"

    def test_ensure_credentials_success(self):
        token_manager = TokenManager(ACCESS_TOKEN, "mock_refresh_token", "mock_api_key")
        try:
            token_manager.ensure_credentials()
        except InvalidCredentialsException as e:
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

            with pytest.raises(TokenRefreshFailedException):
                await token_manager.get_auth_data()

    def test_is_token_valid_malformed_jwt(self):
        manager = TokenManager("not-a-valid-jwt-token", "mock_refresh_token", "mock_api_key")
        assert manager.is_token_valid() is False

    def test_is_token_valid_configurable_buffer(self):
        token = generate_token(45)
        manager_default = TokenManager(token, "mock_refresh_token", "mock_api_key")
        assert manager_default.is_token_valid() is False

        manager_custom = TokenManager(
            token, "mock_refresh_token", "mock_api_key", refresh_buffer_seconds=30.0
        )
        assert manager_custom.is_token_valid() is True

        assert manager_default.is_token_valid(buffer_seconds=30.0) is True
        assert manager_custom.is_token_valid(buffer_seconds=50.0) is False

    @pytest.mark.asyncio
    async def test_refresh_token_concurrent_lock(self):
        token_manager = TokenManager(
            access_token=EXPIRED_ACCESS_TOKEN,
            refresh_token="mock_refresh_token",
            api_key="mock_api_key",
        )
        refresh_url = "https://api.developer.electrolux.one/api/v1/token/refresh"

        with aioresponses() as mocked:
            mocked.post(
                refresh_url,
                payload={
                    "accessToken": NEW_ACCESS_TOKEN,
                    "refreshToken": "new_refresh_token",
                },
            )

            results = await asyncio.gather(
                token_manager.refresh_token(),
                token_manager.refresh_token(),
                token_manager.refresh_token(),
                token_manager.refresh_token(),
                token_manager.refresh_token(),
            )

            assert all(r is True for r in results)
            assert len(mocked.requests[("POST", URL(refresh_url))]) == 1
            assert token_manager._auth_data.access_token == NEW_ACCESS_TOKEN
            assert token_manager._auth_data.refresh_token == "new_refresh_token"

    @pytest.mark.asyncio
    async def test_refresh_token_already_valid_no_force(self):
        token_manager = TokenManager(ACCESS_TOKEN, "mock_refresh_token", "mock_api_key")
        assert await token_manager.refresh_token(force=False) is True

    @pytest.mark.asyncio
    async def test_get_auth_data_force_refresh(self):
        token = generate_token(120)
        token_manager = TokenManager(
            access_token=token,
            refresh_token="mock_refresh_token",
            api_key="mock_api_key",
        )
        refresh_url = "https://api.developer.electrolux.one/api/v1/token/refresh"

        with aioresponses() as mocked:
            auth_data1 = await token_manager.get_auth_data(force_refresh=False)
            assert auth_data1.access_token == token

            mocked.post(
                refresh_url,
                payload={
                    "accessToken": NEW_ACCESS_TOKEN,
                    "refreshToken": "new_refresh_token",
                },
            )
            auth_data2 = await token_manager.get_auth_data(force_refresh=True)
            assert auth_data2.access_token == NEW_ACCESS_TOKEN
            assert auth_data2.refresh_token == "new_refresh_token"

    def test_get_user_id_from_token_decode_error(self):
        with pytest.raises(InvalidTokenException, match="Failed to decode token"):
            get_user_id_from_token("invalid-token-string")

    def test_invalid_grant_exception_hierarchy(self):
        assert issubclass(InvalidGrantException, TokenRefreshFailedException)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status_code", [400, 401])
    async def test_get_auth_data_raises_invalid_grant_on_auth_error(self, status_code):
        token_manager = TokenManager(generate_token(-120), "mock_refresh", "mock_key")
        with aioresponses() as mocked:
            mocked.post("https://api.developer.electrolux.one/api/v1/token/refresh", status=status_code)
            with pytest.raises(InvalidGrantException) as exc_info:
                await token_manager.get_auth_data()
            assert exc_info.value.status_code == status_code

    @pytest.mark.asyncio
    @pytest.mark.parametrize("is_async", [False, True])
    async def test_on_auth_failed_callback(self, is_async):
        called_with = []
        token_manager = TokenManager(
            generate_token(-120), "mock_refresh", "mock_key",
            on_auth_failed=(lambda err: called_with.append(err)) if not is_async else (lambda err: (called_with.append(err), None)[1]),
        )
        if is_async:
            async def async_cb(err):
                called_with.append(err)
            token_manager.on_auth_failed = async_cb

        with aioresponses() as mocked:
            mocked.post("https://api.developer.electrolux.one/api/v1/token/refresh", status=400)
            assert await token_manager.refresh_token() is False

        assert len(called_with) == 1
        assert isinstance(called_with[0], InvalidGrantException)

    @pytest.mark.asyncio
    async def test_on_auth_failed_not_called_on_transient_error(self):
        called = []
        token_manager = TokenManager(
            generate_token(-120), "mock_refresh", "mock_key",
            on_auth_failed=lambda err: called.append(err),
        )
        with aioresponses() as mocked:
            mocked.post("https://api.developer.electrolux.one/api/v1/token/refresh", status=500)
            with pytest.raises(TokenRefreshFailedException) as exc_info:
                await token_manager.get_auth_data()
            assert not isinstance(exc_info.value, InvalidGrantException)
        assert len(called) == 0

    @pytest.mark.asyncio
    async def test_on_auth_failed_callback_exception_isolated(self):
        def faulty_callback(err):
            raise RuntimeError("Buggy user callback")

        token_manager = TokenManager(
            generate_token(-120), "mock_refresh", "mock_key",
            on_auth_failed=faulty_callback,
        )
        with aioresponses() as mocked:
            mocked.post("https://api.developer.electrolux.one/api/v1/token/refresh", status=400)
            assert await token_manager.refresh_token() is False

    def test_is_token_valid_non_numeric_exp(self):
        token = jwt.encode({"sub": "test-user", "exp": "not-a-timestamp"}, "test-secret-at-least-32-bytes-long", algorithm="HS256")
        manager = TokenManager(token, "mock_refresh_token", "mock_api_key")
        assert manager.is_token_valid() is False

    @pytest.mark.asyncio
    async def test_on_auth_failed_callback_does_not_deadlock_on_lock(self):
        """Verify that a callback querying token_manager does not deadlock on _refresh_lock."""
        reentrant_called = []

        async def reentrant_callback(err):
            reentrant_called.append(err)
            # Accessing is_token_valid or lock-requiring methods shouldn't hang
            assert token_manager._refresh_lock.locked() is False

        token_manager = TokenManager(
            generate_token(-120), "mock_refresh", "mock_key",
            on_auth_failed=reentrant_callback,
        )
        with aioresponses() as mocked:
            mocked.post("https://api.developer.electrolux.one/api/v1/token/refresh", status=400)
            assert await token_manager.refresh_token() is False

        assert len(reentrant_called) == 1

    @pytest.mark.asyncio
    async def test_refresh_token_optional_refresh_token_fallback(self):
        """Verify RFC 6749 Section 5.1: if response omits refreshToken, previous refresh token is retained."""
        token_manager = TokenManager(
            access_token=EXPIRED_ACCESS_TOKEN,
            refresh_token="initial_refresh_token",
            api_key="mock_api_key",
        )
        refresh_url = "https://api.developer.electrolux.one/api/v1/token/refresh"

        with aioresponses() as mocked:
            # Server returns ONLY accessToken (no refreshToken in JSON)
            mocked.post(
                refresh_url,
                payload={
                    "accessToken": NEW_ACCESS_TOKEN,
                },
            )
            success = await token_manager.refresh_token()
            assert success is True
            assert token_manager._auth_data.access_token == NEW_ACCESS_TOKEN
            assert token_manager._auth_data.refresh_token == "initial_refresh_token"

    @pytest.mark.asyncio
    async def test_refresh_token_post_revocation_race_condition(self):
        """Verify that if auth_data is cleared while waiting on lock, refresh_token exits cleanly without AttributeError."""
        token_manager = TokenManager(
            access_token=EXPIRED_ACCESS_TOKEN,
            refresh_token="mock_refresh",
            api_key="mock_api_key",
        )
        async with token_manager._refresh_lock:
            # Launch refresh_token while lock is held; passes initial credential check, then waits on lock
            task = asyncio.create_task(token_manager.refresh_token())
            await asyncio.sleep(0.01)
            # Clear auth_data as revoke_token would do
            token_manager._auth_data = None

        # Lock is released, waiting coroutine enters lock and exits cleanly
        result = await task
        assert result is False
