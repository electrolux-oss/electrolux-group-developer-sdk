import asyncio
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

import pytest
from aioresponses import aioresponses
from yarl import URL

from electrolux_group_developer_sdk.auth.auth_data import AuthData
from electrolux_group_developer_sdk.client.appliance_client import ApplianceClient
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.client.dto.appliance_details import ApplianceDetails
from electrolux_group_developer_sdk.client.dto.appliance_state import ApplianceState

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
    assert "external-user-agent ElectroluxGroupDeveloperSDK/0.0.21" in headers["User-Agent"]
