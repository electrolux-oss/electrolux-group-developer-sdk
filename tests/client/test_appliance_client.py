import asyncio
import json
import random
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

import pytest
import aiohttp
from aioresponses import aioresponses
from yarl import URL

from electrolux_group_developer_sdk.auth.auth_data import AuthData
from electrolux_group_developer_sdk.client.appliance_client import ApplianceClient, apply_sse_update
from electrolux_group_developer_sdk.client.bad_credentials_exception import BadCredentialsException
from electrolux_group_developer_sdk.client.client_exception import ApplianceClientException
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.client.dto.appliance_details import ApplianceDetails
from electrolux_group_developer_sdk.client.dto.appliance_state import ApplianceState
from electrolux_group_developer_sdk.client.dto.email import Email
from electrolux_group_developer_sdk.client.dto.livestream_config import LivestreamConfig
from electrolux_group_developer_sdk.client.failed_connection_exception import FailedConnectionException
from electrolux_group_developer_sdk.constants import SDK_VERSION, SDK_USER_AGENT

EXTERNAL_USER_AGENT = "external-user-agent"


class TestApplianceClient():

    @pytest.mark.asyncio
    async def test_rate_limits(self):
        json_path = Path(__file__).parent / "data" / "test_appliances.json"
        with open(json_path) as f:
            payload = json.load(f)

        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with aioresponses() as mocked:
                # Mock the response for the get appliances
                url = "https://api.developer.electrolux.one/api/v1/appliances"
                mocked.get(
                    url,
                    payload=payload,
                    repeat=True
                )

                start = asyncio.get_event_loop().time()

                async def call_get_appliances(i):
                    return await appliance_client.get_appliances()

                # Fire 21 parallel requests
                tasks = [asyncio.create_task(call_get_appliances(i)) for i in range(21)]
                results = await asyncio.gather(*tasks)

                end = asyncio.get_event_loop().time()
                duration = end - start

                # Should take at least 2 seconds for 21 calls @ 10/sec rate
                assert duration >= 2.0

                expected = [Appliance(**item) for item in payload]
                for res in results:
                    assert res == expected
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self):
        json_path = Path(__file__).parent / "data" / "test_appliances.json"
        with open(json_path) as f:
            payload = json.load(f)

        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager, EXTERNAL_USER_AGENT)

            with aioresponses() as mocked:
                # Mock the response for the get appliances
                url = "https://api.developer.electrolux.one/api/v1/appliances"
                mocked.get(
                    url,
                    payload=payload,
                )

                await appliance_client.test_connection()

                # Assertions
                check_header_user_agent(mocked)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status, expected_exception", [
        (401, BadCredentialsException),
        (403, BadCredentialsException),
        (504, FailedConnectionException),
        (429, FailedConnectionException),
    ])
    async def test_test_connection_http_error(self, status, expected_exception):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with aioresponses() as mocked:
                # Mock the response for the get appliances
                url = "https://api.developer.electrolux.one/api/v1/appliances"
                mocked.get(
                    url,
                    status=status,
                    repeat=True
                )

                with pytest.raises(expected_exception):
                    await appliance_client.test_connection()

    @pytest.mark.asyncio
    async def test_get_user_email_success(self):
        json_path = Path(__file__).parent / "data" / "test_user_email.json"
        with open(json_path) as f:
            payload = json.load(f)

        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager, EXTERNAL_USER_AGENT)

            with aioresponses() as mocked:
                # Mock the response for the get appliance info
                url = "https://api.developer.electrolux.one/api/v1/users/current/email"
                mocked.get(
                    url,
                    payload=payload,
                )

                response = await appliance_client.get_user_email()

                # Assertions
                expected_email = Email(**payload)
                assert response == expected_email

                check_header_user_agent(mocked)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status, expected_calls", [
        (401, 1),
        (403, 1),
        (504, 3),
        (429, 3),
    ])
    async def test_get_user_email_request_failed(self, status, expected_calls):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with aioresponses() as mocked:
                # Mock the response for the get appliance info
                url = "https://api.developer.electrolux.one/api/v1/users/current/email"
                mocked.get(
                    url,
                    status=status,
                    repeat=True
                )

                with pytest.raises(ApplianceClientException):
                    await appliance_client.get_user_email()
                assert len(mocked.requests[('GET', URL(url))]) == expected_calls

    @pytest.mark.asyncio
    async def test_get_appliances_success(self):
        json_path = Path(__file__).parent / "data" / "test_appliances.json"
        with open(json_path) as f:
            payload = json.load(f)

        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager, EXTERNAL_USER_AGENT)

            with aioresponses() as mocked:
                # Mock the response for the get appliances
                url = "https://api.developer.electrolux.one/api/v1/appliances"
                mocked.get(
                    url,
                    payload=payload,
                )

                response = await appliance_client.get_appliances()

                # Assertions
                expected_appliances = [Appliance(**item) for item in payload]
                assert response == expected_appliances

                check_header_user_agent(mocked)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status, expected_calls", [
        (401, 1),
        (504, 3),
        (429, 3),
    ])
    async def test_get_appliances_request_failed(self, status, expected_calls):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with aioresponses() as mocked:
                # Mock the response for the get appliances
                url = "https://api.developer.electrolux.one/api/v1/appliances"
                mocked.get(
                    url,
                    status=status,
                    repeat=True
                )

                with pytest.raises(Exception):
                    await appliance_client.get_appliances()

                assert len(mocked.requests[('GET', URL(url))]) == expected_calls

    @pytest.mark.asyncio
    async def test_get_appliance_details_success(self):
        json_path = Path(__file__).parent / "data" / "test_appliance_info.json"
        with open(json_path) as f:
            payload = json.load(f)

        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager, EXTERNAL_USER_AGENT)

            with aioresponses() as mocked:
                # Mock the response for the get appliance info
                url = "https://api.developer.electrolux.one/api/v1/appliances/999011524_00:94700001-443E07021CE1/info"
                mocked.get(
                    url,
                    payload=payload,
                )

                response = await appliance_client.get_appliance_details("999011524_00:94700001-443E07021CE1")

                # Assertions
                expected_appliance_info = ApplianceDetails(**payload)
                assert response == expected_appliance_info

                check_header_user_agent(mocked)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status, expected_calls", [
        (401, 1),
        (504, 3),
        (429, 3),
    ])
    async def test_get_appliance_details_request_failed(self, status, expected_calls):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with aioresponses() as mocked:
                # Mock the response for the get appliance info
                url = "https://api.developer.electrolux.one/api/v1/appliances/999011524_00:94700001-443E07021CE1/info"
                mocked.get(
                    url,
                    status=status,
                    repeat=True
                )

                with pytest.raises(Exception):
                    await appliance_client.get_appliance_details("999011524_00:94700001-443E07021CE1")
                assert len(mocked.requests[('GET', URL(url))]) == expected_calls

    @pytest.mark.asyncio
    async def test_get_appliance_details_missing_applianceid(self):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with pytest.raises(ValueError):
                await appliance_client.get_appliance_details(None)

    @pytest.mark.asyncio
    async def test_get_appliance_state_success(self):
        json_path = Path(__file__).parent / "data" / "test_appliance_state.json"
        with open(json_path) as f:
            payload = json.load(f)

        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager, EXTERNAL_USER_AGENT)

            with aioresponses() as mocked:
                # Mock the response for the get appliance state
                url = "https://api.developer.electrolux.one/api/v1/appliances/999011524_00:94700001-443E07021CE1/state"
                mocked.get(
                    url,
                    payload=payload,
                )

                response = await appliance_client.get_appliance_state("999011524_00:94700001-443E07021CE1")

                # Assertions
                expected_appliance_state = ApplianceState(**payload)
                assert response == expected_appliance_state

                check_header_user_agent(mocked)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status, expected_calls", [
        (401, 1),
        (504, 3),
        (429, 3),
    ])
    async def test_get_appliance_state_request_failed(self, status, expected_calls):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with aioresponses() as mocked:
                # Mock the response for the get appliance state
                url = "https://api.developer.electrolux.one/api/v1/appliances/999011524_00:94700001-443E07021CE1/state"
                mocked.get(
                    url,
                    status=status,
                    repeat=True
                )

                with pytest.raises(Exception):
                    await appliance_client.get_appliance_state("999011524_00:94700001-443E07021CE1")

                assert len(mocked.requests[('GET', URL(url))]) == expected_calls

    @pytest.mark.asyncio
    async def test_get_appliance_state_missing_appliance_id(self):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with pytest.raises(ValueError):
                await appliance_client.get_appliance_state(None)

    @pytest.mark.asyncio
    async def test_send_command_success(self):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager, EXTERNAL_USER_AGENT)

            with aioresponses() as mocked:
                # Mock the response for the send a command
                url = "https://api.developer.electrolux.one/api/v1/appliances/999011524_00:94700001-443E07021CE1/command"
                request_body = {
                    "executeCommand": "ON"
                }
                mocked.put(
                    url,
                    status=200
                )

                await appliance_client.send_command("999011524_00:94700001-443E07021CE1", request_body)

                calls = mocked.requests.get(('PUT', URL(url)))
                assert len(calls) == 1
                sent_body = calls[0][1].get("json")
                assert sent_body == request_body

                check_header_user_agent(mocked)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status, expected_calls", [
        (401, 1),
        (504, 3),
        (429, 3),
    ])
    async def test_send_command_request_failed(self, status, expected_calls):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with aioresponses() as mocked:
                # Mock the response for the send a command
                url = "https://api.developer.electrolux.one/api/v1/appliances/999011524_00:94700001-443E07021CE1/command"
                request_body = {
                    "executeCommand": "ON"
                }
                mocked.put(
                    url,
                    status=status,
                    repeat=True
                )

                with pytest.raises(Exception):
                    await appliance_client.send_command("999011524_00:94700001-443E07021CE1", request_body)

                assert len(mocked.requests[('PUT', URL(url))]) == expected_calls

    @pytest.mark.asyncio
    async def test_send_command_missing_appliance_id(self):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            request_body = {
                "executeCommand": "ON"
            }

            with pytest.raises(ValueError):
                await appliance_client.send_command(None, request_body)

    @pytest.mark.asyncio
    async def test_send_command_missing_body(self):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with pytest.raises(ValueError):
                await appliance_client.send_command("applianceId", None)

    @pytest.mark.asyncio
    async def test_get_interactive_maps_success(self):
        json_path = Path(__file__).parent / "data" / "test_interactive_map.json"
        with open(json_path) as f:
            payload = json.load(f)

        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager, EXTERNAL_USER_AGENT)

            with aioresponses() as mocked:
                # Mock the response for the get appliances
                url = "https://api.developer.electrolux.one/api/v1/appliances/900277470108000101100106/interactiveMap"
                mocked.get(
                    url,
                    payload=payload,
                )

                response = await appliance_client.get_interactive_maps("900277470108000101100106")

                # Assertions
                assert response == payload

                check_header_user_agent(mocked)

    @pytest.mark.asyncio
    async def test_get_interactive_maps_request_failed(self):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with aioresponses() as mocked:
                # Mock the response for the get appliances
                url = "https://api.developer.electrolux.one/api/v1/appliances/900277470108000101100106/interactiveMap"
                mocked.get(
                    url,
                    status=401
                )

                with pytest.raises(Exception):
                    await appliance_client.get_interactive_maps("900277470108000101100106")

    @pytest.mark.asyncio
    async def test_get_memory_maps_success(self):
        json_path = Path(__file__).parent / "data" / "test_memory_map.json"
        with open(json_path) as f:
            payload = json.load(f)

        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager, EXTERNAL_USER_AGENT)

            with aioresponses() as mocked:
                # Mock the response for the get appliances
                url = "https://api.developer.electrolux.one/api/v1/appliances/900277470108000101100106/memoryMap"
                mocked.get(
                    url,
                    payload=payload,
                )

                response = await appliance_client.get_memory_maps("900277470108000101100106")

                # Assertions
                assert response == payload

                check_header_user_agent(mocked)

    @pytest.mark.asyncio
    async def test_get_memory_maps_request_failed(self):
        mock_token_manager = MagicMock()

        with patch("electrolux_group_developer_sdk.auth.token_manager.TokenManager", return_value=mock_token_manager):
            mock_token_manager.get_auth_data = AsyncMock(return_value=AuthData(
                access_token="mock_access_token",
                refresh_token="mock_refresh_token",
                api_key="mock_api_key"
            ))
            appliance_client = ApplianceClient(mock_token_manager)

            with aioresponses() as mocked:
                # Mock the response for the get appliances
                url = "https://api.developer.electrolux.one/api/v1/appliances/900277470108000101100106/memoryMap"
                mocked.get(
                    url,
                    status=401
                )

                with pytest.raises(Exception):
                    await appliance_client.get_memory_maps("900277470108000101100106")


def check_header_user_agent(mocked):
    method, url_key = next(iter(mocked.requests.keys()))
    calls = mocked.requests[(method, url_key)]
    request_call = calls[0]
    headers = request_call.kwargs.get("headers", {})

    # Check headers
    assert "User-Agent" in headers
    assert f"external-user-agent {SDK_USER_AGENT}/{SDK_VERSION}" in headers["User-Agent"]


def test_apply_sse_update():
    appliance_state_path = Path(__file__).parent / "data" / "test_appliance_state.json"
    updated_appliance_state_path = Path(__file__).parent / "data" / "test_appliance_state_updated.json"
    state_event_path = Path(__file__).parent / "data" / "test_state_event.json"

    with open(appliance_state_path) as f:
        state = ApplianceState(**json.load(f))
    with open(updated_appliance_state_path) as f:
        expected_updated_state = ApplianceState(**json.load(f))
    with open(state_event_path) as f:
        state_event = json.load(f)
    
    updated_state = apply_sse_update(state, state_event)

    assert updated_state == expected_updated_state

def test_apply_sse_update_connectivity_state():
    appliance_state_path = Path(__file__).parent / "data" / "test_appliance_state.json"
    updated_appliance_state_path = Path(__file__).parent / "data" / "test_appliance_state_updated_connection.json"
    state_event_path = Path(__file__).parent / "data" / "test_state_event_connection.json"

    with open(appliance_state_path) as f:
        state = ApplianceState(**json.load(f))
    with open(updated_appliance_state_path) as f:
        expected_updated_state = ApplianceState(**json.load(f))
    with open(state_event_path) as f:
        state_event = json.load(f)
    
    updated_state = apply_sse_update(state, state_event)

    assert updated_state == expected_updated_state


@pytest.mark.asyncio
async def test_start_event_stream_dispatch_and_callbacks():
    """Verify that start_event_stream invokes opening callbacks and dispatches SSE events to registered listeners."""
    mock_token_manager = MagicMock()
    mock_token_manager.get_auth_data = AsyncMock(
        return_value=AuthData(
            access_token="mock_token", refresh_token="mock_refresh", api_key="mock_key"
        )
    )
    client = ApplianceClient(mock_token_manager)
    client.get_livestream_config = AsyncMock(
        return_value=LivestreamConfig(
            url="https://api.developer.electrolux.one/livestream", appliances=[]
        )
    )

    received_events = []
    opening_callback_called = []

    async def opening_callback():
        opening_callback_called.append(True)

    def event_listener(event):
        received_events.append(event)

    client.add_listener("test_app_1", event_listener)

    # Use native aiohttp.StreamReader to simulate SSE stream
    protocol = MagicMock()
    reader = aiohttp.StreamReader(protocol, limit=2**16)
    reader.feed_data(
        b'data: {"applianceId": "test_app_1", "property": "timeToEnd", "value": 120}\n\n'
    )
    reader.feed_eof()

    mock_resp = MagicMock()
    mock_resp.closed = False
    mock_resp.content = reader

    mock_session = MagicMock()
    mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_session.get.return_value.__aexit__ = AsyncMock()
    mock_session.close = AsyncMock()

    async def fake_sleep(duration):
        raise asyncio.CancelledError()

    with patch("aiohttp.ClientSession", return_value=mock_session):
        with patch.object(asyncio, "sleep", side_effect=fake_sleep):
            with pytest.raises(asyncio.CancelledError):
                await client.start_event_stream(
                    do_on_livestream_opening_list=[opening_callback]
                )

    assert len(opening_callback_called) == 1
    assert len(received_events) == 1
    assert received_events[0] == {
        "applianceId": "test_app_1",
        "property": "timeToEnd",
        "value": 120,
    }


@pytest.mark.asyncio
async def test_start_event_stream_progressive_backoff():
    """Verify that start_event_stream applies progressive exponential backoff on reconnection attempts."""
    mock_token_manager = MagicMock()
    mock_token_manager.get_auth_data = AsyncMock(
        return_value=AuthData(
            access_token="mock_token", refresh_token="mock_refresh", api_key="mock_key"
        )
    )
    client = ApplianceClient(mock_token_manager)
    client.get_livestream_config = AsyncMock(
        return_value=LivestreamConfig(
            url="https://api.developer.electrolux.one/livestream", appliances=[]
        )
    )

    sleep_calls = []

    async def fake_sleep(duration):
        sleep_calls.append(duration)
        if len(sleep_calls) >= 3:
            raise asyncio.CancelledError()

    mock_session = MagicMock()
    mock_session.get.side_effect = ConnectionError("Mock connection failed")
    mock_session.close = AsyncMock()

    with patch("aiohttp.ClientSession", return_value=mock_session):
        with patch.object(asyncio, "sleep", side_effect=fake_sleep):
            with patch.object(random, "uniform", return_value=1.0):
                with pytest.raises(asyncio.CancelledError):
                    await client.start_event_stream(
                        initial_backoff=1.0, max_backoff=60.0, backoff_factor=2.0
                    )

    # Verify exponential progression: 1.0s, 2.0s, 4.0s
    assert len(sleep_calls) == 3
    assert sleep_calls[0] == pytest.approx(1.0)
    assert sleep_calls[1] == pytest.approx(2.0)
    assert sleep_calls[2] == pytest.approx(4.0)
