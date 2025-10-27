import asyncio
import json
import logging

from electrolux_group_developer_sdk.auth.token_manager import TokenManager
from electrolux_group_developer_sdk.client.appliance_client import ApplianceClient

_LOGGER = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.INFO)

    print("Please enter your credentials:")

    access_token = input("Access Token: ").strip()
    refresh_token = input("Refresh Token: ").strip()
    api_key = input("API Key: ").strip()

    # Initialize TokenManager
    token_manager = TokenManager(access_token, refresh_token, api_key)

    print("Credentials stored successfully.")

    appliance_client = ApplianceClient(token_manager)

    while True:
        print("\nChoose an option:")
        print("1. Refresh token")
        print("2. Revoke token")
        print("3. Get Appliances")
        print("4. Get Appliance info")
        print("5. Get Appliance state")
        print("6. Send commands")
        print("7. Get interactive map")
        print("8. Get memory map")
        print("9. Update auth data")
        print("10. Exceed rate limit")
        print("11. Start SSE stream")
        print("12. Exit")

        choice = input("> ").strip()

        if choice == "1":
            try:
                response = await token_manager.refresh_token()
                print("Response:", response)
            except Exception as e:
                print(f"Error refreshing token: {e}")
        elif choice == "2":
            try:
                response = await token_manager.revoke_token()
                print("Response:", response)
            except Exception as e:
                print(f"Error revoking token: {e}")
        elif choice == "3":
            try:
                response = await appliance_client.get_appliances()
                print("Appliances:", response)
            except Exception as e:
                print(f"Error fetching appliances: {e}")
        elif choice == "4":
            try:
                appliance_id = input("Please enter the applianceId: ").strip()
                response = await appliance_client.get_appliance_details(appliance_id)
                print("Appliance info:", response)
            except Exception as e:
                print(f"Error fetching appliance info: {e}")
        elif choice == "5":
            try:
                appliance_id = input("ApplianceId: ").strip()
                response = await appliance_client.get_appliance_state(appliance_id)
                print("Appliances:", response)
            except Exception as e:
                print(f"Error fetching appliance state: {e}")
        elif choice == "6":
            try:
                appliance_id = input("ApplianceId: ").strip()
                commands = input("Commands: ").strip()
                response = await appliance_client.send_command(appliance_id, json.loads(commands))
                print("Send command:", response)
            except Exception as e:
                print(f"Error sending commands: {e}")
        elif choice == "7":
            try:
                appliance_id = input("ApplianceId: ").strip()
                response = await appliance_client.get_interactive_maps(appliance_id)
                print("Interactive maps:", response)
            except Exception as e:
                print(f"Error fetching interactive maps: {e}")
        elif choice == "8":
            try:
                appliance_id = input("ApplianceId: ").strip()
                response = await appliance_client.get_memory_maps(appliance_id)
                print("Memory maps:", response)
            except Exception as e:
                print(f"Error fetching memory maps: {e}")
        elif choice == "9":
            try:
                access_token = input("Access Token: ").strip()
                refresh_token = input("Refresh Token: ").strip()
                api_key = input("API Key: ").strip()
                await token_manager.update(access_token, refresh_token, api_key)
                print("Auth data updated")
            except Exception as e:
                print(f"Error exceeding rate limit: {e}")
        elif choice == "10":
            try:
                await exceed_rate_limit(appliance_client, count=5)
            except Exception as e:
                print(f"Error updating auth data: {e}")
        elif choice == "11":
            try:
                def handle_event(event) -> None:
                    print("SSE event received:", event)
                appliance_client.add_listener("applianceId", handle_event)
                await appliance_client.start_event_stream()
            except Exception as e:
                print(f"Error starting SSE: {e}")
        elif choice == "12":
            print("Exiting.")
            break
        else:
            print("Invalid option. Try again.")


async def exceed_rate_limit(appliance_client, count):
    async def call_get_appliances(i):
        try:
            await appliance_client.get_appliance_data()
        except Exception as e:
            print(f"[{i}] Failed: {e}")

    tasks = [asyncio.create_task(call_get_appliances(i)) for i in range(count)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
