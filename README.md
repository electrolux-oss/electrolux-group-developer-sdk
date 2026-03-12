# Electrolux Group Developer SDK

The official Python async client library for interacting with the **Electrolux Developer Portal API**.  
This library handles authentication, token management, and communication with appliances (e.g. getting appliance info,
state, and sending commands).

---

## 🚀 Features

- Async API client powered by `aiohttp`
- JWT expiry check
- Automatic token management
- Easy appliance access (list, details, state)
- Command sending interface

## 🔧 CLI

This library includes a CLI tool to manually test and interact with the API.

## 📑 Authentication

To use this library, you must have credentials from
the [Electrolux Developer Portal](https://developer.electrolux.one/):

1. **Log in to the developer portal** you need an Electrolux Group account with a password. If you don't have one, you
   can create it from one of Electrolux Group apps.

2. **Create an API Key** for your account.

3. **Generate an Access Token and Refresh Token** using the portal.

4. Use these credentials in your app or provide them to the CLI when prompted.

# ⚡ Quickstart

This example demonstrates how to authenticate and fetch your appliance data:

```python
import asyncio
from electrolux_group_developer_sdk.auth.token_manager import TokenManager
from electrolux_group_developer_sdk.client.appliance_client import ApplianceClient


# Callback to handle token updates
def on_token_update(new_access_token, new_refresh_token, api_key):
    # Save updated tokens somewhere safe
    print("Access Token updated:", new_access_token)
    print("Refresh Token updated:", new_refresh_token)
    print("API Key:", api_key)

async def main():
    # Initialize the token manager
    token_manager = TokenManager(
        access_token="your_access_token",
        refresh_token="your_refresh_token",
        api_key="your_api_key",
        on_token_update=on_token_update
    )

    # Initialize the appliance client
    appliance_client = ApplianceClient(token_manager=token_manager)

    # Fetch all your appliances
    appliance_list = await appliance_client.get_appliance_data()

    # appliance_list is a list of ApplianceData objects
    for appliance in appliance_list:
        print(appliance)

# Run the async main function
asyncio.run(main())
```
## Notes
- `ElectroluxTokenManager` handles token refreshing automatically.
- `on_token_update` callback is called whenever tokens are refreshed.
- `get_appliance_data()` is async and returns a list of `ApplianceData` objects representing your owned appliances.
