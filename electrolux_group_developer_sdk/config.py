BASE_API_URL = "https://api.developer.electrolux.one"

TOKEN_REFRESH_URL = f"{BASE_API_URL}/api/v1/token/refresh"
TOKEN_REVOKE_URL = f"{BASE_API_URL}/api/v1/token/revoke"

GET_APPLIANCES_URL = f"{BASE_API_URL}/api/v1/appliances"
GET_APPLIANCE_STATE_URL = f"{BASE_API_URL}/api/v1/appliances/{{appliance_id}}/state"
GET_APPLIANCE_INFO_URL = f"{BASE_API_URL}/api/v1/appliances/{{appliance_id}}/info"
SEND_COMMAND_URL = f"{BASE_API_URL}/api/v1/appliances/{{appliance_id}}/command"
GET_INTERACTIVE_MAPS_URL = f"{BASE_API_URL}/api/v1/appliances/{{appliance_id}}/interactiveMap"
GET_MEMORY_MAPS_URL = f"{BASE_API_URL}/api/v1/appliances/{{appliance_id}}/memoryMap"
GET_LIVESTREAM_CONFIG_URL = f"{BASE_API_URL}/api/v1/configurations/livestream"
