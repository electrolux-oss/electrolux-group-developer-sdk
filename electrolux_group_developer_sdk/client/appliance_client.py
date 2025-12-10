import asyncio
import json
import logging
from collections.abc import Awaitable, Callable
from typing import Optional, Dict, Any, List

import aiohttp
from aiohttp import ClientTimeout, ClientResponseError
from aiohttp.hdrs import USER_AGENT, AUTHORIZATION

from .appliance_data_factory import appliance_data_factory
from .client_exception import ApplianceClientException
from .client_util import request
from .dto.appliance import Appliance
from .dto.appliance_details import ApplianceDetails
from .dto.appliance_state import ApplianceState
from .dto.interactive_map import InteractiveMap
from .dto.livestream_config import LivestreamConfig
from .dto.memory_map import MemoryMap
from .failed_connection_exception import FailedConnectionException
from ..auth.token_manager import TokenManager
from ..client.appliances.appliance_data import ApplianceData
from ..config import (
    GET_APPLIANCES_URL,
    GET_APPLIANCE_INFO_URL,
    GET_APPLIANCE_STATE_URL,
    SEND_COMMAND_URL,
    GET_INTERACTIVE_MAPS_URL,
    GET_MEMORY_MAPS_URL,
    GET_LIVESTREAM_CONFIG_URL,
)
from ..constants import API_KEY, GET, PUT, SDK_USER_AGENT, SDK_VERSION

_LOGGER = logging.getLogger(__name__)

def _is_dam_appliance(appliance_id):
    if appliance_id.startswith("1:"):
        return True
    else:
        return False


def _build_user_agent(external_user_agent: Optional[str] = None) -> str:
    sdk_version = SDK_VERSION

    sdk_user_agent = f"{SDK_USER_AGENT}/{sdk_version}"

    if external_user_agent:
        return f"{external_user_agent} {sdk_user_agent}"

    return sdk_user_agent


class ApplianceClient:
    """
    Client for interacting with the Electrolux Developer API to manage and retrieve appliance data.

    This class provides asynchronous methods to fetch the list of appliances, detailed appliance info,
    and appliance state, using authentication managed by the provided AuthClient.

    Attributes:
        _token_manager (TokenManager)
    """

    def __init__(self, token_manager: TokenManager, external_user_agent: Optional[str] = None):
        """
        Initialize the ApplianceClient.

        Args:
            token_manager (TokenManager): TokenManager for handling authenticated requests.
            external_user_agent (str, optional): An optional user agent string to append
                to the SDK's default User-Agent header when making the request. This allows
                external applications to identify themselves in API calls. If not provided,
                only the SDK's default user agent is used.
        """
        self._token_manager = token_manager
        self._sse_listeners: dict[str, list[Callable[[dict], None]]] = {}
        self._external_user_agent = external_user_agent

    async def test_connection(self) -> None:
        try:
            await self._send_authorized_request(GET, GET_APPLIANCES_URL)
        except ApplianceClientException as e:
            _LOGGER.error("Test connection failed: %s", e)
            raise FailedConnectionException(f"Failed connection.", status_code=e.status)
        except ClientResponseError as e:
            _LOGGER.error("Test connection failed: %s", e)
            raise FailedConnectionException(f"Failed connection.", status_code=e.status)
        except Exception as e:
            _LOGGER.error("Test connection failed: %s", e)
            raise FailedConnectionException("Failed connection.")

    async def get_appliance_data(self) -> list[ApplianceData]:
        """Retrieve all the appliances data, returning specific appliance types when available."""
        appliances = await self.get_appliances()

        appliance_list = []
        for appliance in appliances:
            try:
                details = await self.get_appliance_details(appliance.applianceId)
            except ApplianceClientException as e:
                details = None
                _LOGGER.warning(
                    "Failed to get details for %s: %s", appliance.applianceId, e
                )

            try:
                state = await self.get_appliance_state(appliance.applianceId)
            except ApplianceClientException as e:
                state = None
                _LOGGER.warning(
                    "Failed to get state for %s: %s", appliance.applianceId, e
                )

            appliance_data = appliance_data_factory(
                appliance=appliance,
                details=details,
                state=state,
            )

            appliance_list.append(appliance_data)

        return appliance_list

    async def get_appliances(self) -> list[Appliance]:
        """
        Retrieve a list of appliances associated with the authenticated user.

        Returns:
            List[Appliance]: List of appliances.

        Raises:
            ApplianceClientException: If the request to fetch appliances fails.
        """
        try:
            response = await self._send_authorized_request(GET, GET_APPLIANCES_URL)
            appliances = [Appliance(**item) for item in response]
            return appliances
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Failed to get appliances: %s", e)
            raise ApplianceClientException(
                f"Failed to get appliances: {e}", status=e.status
            ) from e
        except Exception as e:
            _LOGGER.error("Failed to get appliances: %s", e)
            raise ApplianceClientException(f"Failed to get appliances: {e}")

    async def get_appliance_details(self, appliance_id: str) -> ApplianceDetails:
        """
        Retrieve detailed information about a specific appliance.

        Args:
            appliance_id (str): The ID of the appliance to retrieve information for.

        Returns:
            ApplianceDetails: Detailed information of the appliance.

        Raises:
            ValueError: If `appliance_id` is not provided.
            ApplianceClientException: If the request to fetch appliance info fails.
        """
        if not appliance_id:
            raise ValueError("applianceId is required")

        url = GET_APPLIANCE_INFO_URL.format(appliance_id=appliance_id)

        try:
            response = await self._send_authorized_request(GET, url)
            return ApplianceDetails(**response)
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Error during get appliance info: %s", e)
            raise ApplianceClientException(
                f"Failed to get appliance info: {e}", status=e.status
            ) from e
        except Exception as e:
            _LOGGER.error("Error during get appliance info: %s", e)
            raise ApplianceClientException(f"Failed to get appliance info: {e}")

    async def get_appliance_state(self, appliance_id: str) -> ApplianceState:
        """
        Retrieve the current state of a specific appliance.

        Args:
            appliance_id (str): The ID of the appliance to retrieve state for.

        Returns:
            ApplianceState: The current state of the appliance.

        Raises:
            ValueError: If `appliance_id` is not provided.
            ApplianceClientException: If the request to fetch appliance state fails.
        """
        if not appliance_id:
            raise ValueError("applianceId is required")

        url = GET_APPLIANCE_STATE_URL.format(appliance_id=appliance_id)

        try:
            response = await self._send_authorized_request(GET, url)

            if not response:
                _LOGGER.error(
                    "Empty response while getting appliance state for %s", appliance_id
                )
                raise ApplianceClientException("Empty response from Electrolux API")

            return ApplianceState(**response)
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Error during get appliance state: %s", e)
            raise ApplianceClientException(
                f"Failed to get appliance state: {e}", status=e.status
            ) from e
        except Exception as e:
            _LOGGER.error("Error during get appliance state: %s", e)
            raise ApplianceClientException(f"Failed to get appliance state: {e}")

    async def send_command(self, appliance_id: str, commands: dict[str, Any]) -> Any:
        """
        Send a command to the appliance.

        Args:
            appliance_id (str): The ID of the appliance to send the command to.
            commands (dict): The command to be sent to the appliance.

        Raises:
            ValueError: If `appliance_id` or `commands` are not provided.
            ApplianceClientException: If the request to send command fails.
        """
        if not appliance_id:
            raise ValueError("applianceId is required")
        if not commands:
            raise ValueError("commands body is required")

        url = SEND_COMMAND_URL.format(appliance_id=appliance_id)

        if _is_dam_appliance(appliance_id):
            commands = {"commands": [commands]}

        try:
            response = await self._send_authorized_request(PUT, url, commands)
            return response
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Error sending command: %s", e)
            raise ApplianceClientException(
                f"Failed to send command: {e}", status=e.status
            ) from e
        except Exception as e:
            _LOGGER.error("Error sending command: %s", e)
            raise ApplianceClientException(f"Failed to send command: {e}")

    async def get_interactive_maps(self, appliance_id: str) -> list[dict[str, Any]]:
        """
        Retrieve interactive maps for a given appliance ID.

        Args:
            appliance_id (str): The unique ID of the appliance.

        Returns:
            list[dict]: A list of interactive map data as JSON-serializable dictionaries.

        Raises:
            ValueError: If `appliance_id` is not provided.
            ApplianceClientException: If the API request fails or returns invalid data.
        """
        if not appliance_id:
            raise ValueError("applianceId is required")

        url = GET_INTERACTIVE_MAPS_URL.format(appliance_id=appliance_id)

        try:
            response = await self._send_authorized_request(GET, url)
            maps = [InteractiveMap(**item) for item in response]
            maps_dict = [m.model_dump(mode="json") for m in maps]

            return maps_dict
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Error during get interactive map: %s", e)
            raise ApplianceClientException(
                f"Failed to get interactive maps: {e}", status=e.status
            ) from e
        except Exception as e:
            _LOGGER.error("Error during get interactive map: %s", e)
            raise ApplianceClientException(f"Failed to get interactive maps: {e}")

    async def get_memory_maps(self, appliance_id: str) -> list[dict[str, Any]]:
        """
        Retrieve memory maps for a given appliance ID.

        Args:
            appliance_id (str): The unique ID of the appliance.

        Returns:
            list[dict]: A list of memory map data as JSON-serializable dictionaries.

        Raises:
            ValueError: If `appliance_id` is not provided.
            ApplianceClientException: If the API request fails or returns invalid data.
        """
        if not appliance_id:
            raise ValueError("applianceId is required")

        url = GET_MEMORY_MAPS_URL.format(appliance_id=appliance_id)

        try:
            response = await self._send_authorized_request(GET, url)
            maps = [MemoryMap(**item) for item in response]
            maps_dict = [m.model_dump(mode="json") for m in maps]

            return maps_dict
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Error during get memory maps: %s", e)
            raise ApplianceClientException(
                f"Failed to get memory maps: {e}", status=e.status
            ) from e
        except Exception as e:
            _LOGGER.error("Error during get memory maps: %s", e)
            raise ApplianceClientException(f"Failed to get memory maps: {e}")

    async def get_livestream_config(self) -> LivestreamConfig:
        url = GET_LIVESTREAM_CONFIG_URL
        try:
            response = await self._send_authorized_request(GET, url)
            config = LivestreamConfig(**response)
            return config
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Error during get livestream config: %s", e)
            raise ApplianceClientException(
                f"Failed to get livestream config: {e}", status=e.status
            ) from e
        except Exception as e:
            _LOGGER.error("Error during get livestream config: %s", e)
            raise ApplianceClientException(f"Failed to livestream config: {e}")

    async def start_event_stream(self,
                                 do_on_livestream_opening_list: Optional[List[Callable[[], Awaitable[None]]]] = None):
        """Open SSE connection and stream appliance events indefinitely."""
        livestream_config = await self.get_livestream_config()
        url = livestream_config.url

        while True:
            websession = aiohttp.ClientSession()  # create a new session each retry
            try:
                auth_data = await self._token_manager.get_auth_data()
                headers = {
                    AUTHORIZATION: f"Bearer {auth_data.access_token}",
                    API_KEY: auth_data.api_key,
                }

                async with websession.get(
                        url,
                        timeout=ClientTimeout(total=None, sock_connect=5, sock_read=None),
                        headers=headers,
                ) as resp:
                    _LOGGER.info("Connected to SSE stream at %s", url)

                    if do_on_livestream_opening_list:
                        _LOGGER.info("Calling do_on_livestream_opening callbacks.")
                        for callback in do_on_livestream_opening_list:
                            await callback()

                    while True:
                        data_line = None

                        while True:  # read one SSE event
                            if resp.closed:
                                _LOGGER.warning("SSE connection object closed")
                                raise ConnectionError("SSE response stream closed unexpectedly")

                            line = await asyncio.wait_for(
                                resp.content.readline(), timeout=120
                            )

                            if not line:
                                _LOGGER.warning("SSE connection ended by server")
                                raise ConnectionError("SSE connection closed by server")

                            line_str = line.decode().strip()

                            if line_str.startswith("data:"):
                                data_line = line_str.removeprefix("data:").strip()
                            elif line_str == "":
                                break

                        if not data_line:
                            continue

                        try:
                            event = json.loads(data_line)
                        except json.JSONDecodeError:
                            _LOGGER.error("Failed to decode SSE JSON: %s", data_line)
                            continue

                        appliance_id = event.get("applianceId")
                        if not appliance_id:
                            continue

                        for callback in self._sse_listeners.get(appliance_id, []):
                            try:
                                callback(event)
                            except Exception:
                                _LOGGER.exception(
                                    "Listener for %s failed", appliance_id
                                )

            except aiohttp.ClientResponseError as ex:
                _LOGGER.error("SSE error: %s - %s", ex.status, ex.message)
                await asyncio.sleep(10)
            except ConnectionError as ex:
                _LOGGER.error("SSE connection error: %s", ex)
                await asyncio.sleep(10)
            except Exception as ex:
                _LOGGER.error("Unexpected SSE error: %s", ex)
                await asyncio.sleep(10)
            finally:
                _LOGGER.info("Close websession")
                await websession.close()

    def add_listener(self, appliance_id: str, callback: Callable[[dict], None]) -> None:
        """Register a callback for a specific appliance."""
        _LOGGER.info("Add listener for: %s", appliance_id)

        self._sse_listeners.setdefault(appliance_id, []).append(callback)

    def remove_listener(self, appliance_id: str, callback: Callable[[dict], None]) -> None:
        """Unregister a callback."""
        _LOGGER.info("Remove listener for: %s", appliance_id)

        if appliance_id in self._sse_listeners:
            self._sse_listeners[appliance_id].remove(callback)
            if not self._sse_listeners[appliance_id]:
                del self._sse_listeners[appliance_id]

    def remove_all_listeners_by_appliance_id(self, appliance_id: str) -> None:
        """Remove all SSE listeners for a specific appliance."""
        _LOGGER.info("Remove all listeners for appliance %s", appliance_id)

        if appliance_id in self._sse_listeners:
            self._sse_listeners.pop(appliance_id)

    async def _send_authorized_request(
            self, method: str, url: str, json_body: Optional[Dict[str, Any]] = None
    ):
        auth_data = await self._token_manager.get_auth_data()
        user_agent = _build_user_agent(self._external_user_agent)
        headers = {
            AUTHORIZATION: f"Bearer {auth_data.access_token}",
            API_KEY: auth_data.api_key,
            USER_AGENT: user_agent
        }

        return await request(
            method=method, url=url, headers=headers, json_body=json_body
        )
