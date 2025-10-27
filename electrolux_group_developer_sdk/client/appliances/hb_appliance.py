from typing import Any

from pydantic import PrivateAttr

from ...appliance_config.hb_config import HbConfig, HbConfigManager, HOB_HOOD, HOOD_FAN_SPEED, HOOD_STATE, \
    KEY_SOUND_TONE, CHILD_LOCK
from ...client.appliances.appliance_data import ApplianceData
from ...constants import REPORTED


class HBAppliance(ApplianceData):
    """
    Extended appliance data class for HB (Hob) appliances.

    Adds access to capabilities and state via HbConfig.
    """
    _config: HbConfig = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        capabilities = self.details.capabilities if self.details else {}
        self._config = HbConfigManager().get_config(self.appliance.applianceType, capabilities)

    def is_feature_supported(self, feature) -> bool:
        return self._config.is_capability_supported(feature)

    def is_hood_feature_supported(self, feature: str) -> bool:
        return self._config.is_hood_capability_supported(feature)

    def is_hob_zone_feature_supported(self, hob_zone: str, feature: str) -> bool:
        return self._config.is_hob_zone_capability_supported(hob_zone, feature)

    def get_supported_hood_fan_speed(self) -> list[str]:
        """Return the list of supported hood fan speed."""
        return self._config.get_supported_hood_fan_speed()

    def get_available_hob_zone(self) -> list[str]:
        """Return the list of available hob zone from state."""
        return self._config.get_available_hob_zone(self.state.properties.get(REPORTED))

    def get_supported_hood_state(self) -> list[str]:
        """Return the list of supported hood state."""
        return self._config.get_supported_hood_state()

    def get_supported_key_sound_tone(self) -> list[str]:
        """Return the list of supported key sound tone."""
        return self._config.get_supported_key_sound_tone()

    def get_current_hood_fan_speed(self) -> str:
        """Return the current hood fan speed."""
        return self._config.get_current_hood_fan_speed(self.state.properties.get(REPORTED))

    def get_current_hood_state(self) -> str:
        """Return the current hood state."""
        return self._config.get_current_hood_state(self.state.properties.get(REPORTED))

    def get_current_key_sound_tone(self) -> str:
        """Return the current key sound tone."""
        return self._config.get_current_key_sound_tone(self.state.properties.get(REPORTED))

    def get_current_child_lock(self) -> bool:
        """Return the current child lock."""
        return self._config.get_current_child_lock(self.state.properties.get(REPORTED))

    def get_current_appliance_state(self) -> str:
        """Return the current appliance state."""
        return self._config.get_current_appliance_state(self.state.properties.get(REPORTED))

    def get_current_alerts(self) -> list[str]:
        """Return the current alerts."""
        return self._config.get_current_alerts(self.state.properties.get(REPORTED))

    def get_current_remote_control(self) -> str:
        """Return the current remote control."""
        return self._config.get_current_remote_control(self.state.properties.get(REPORTED))

    def get_current_ui_lock_mode(self) -> bool:
        """Return the current ui lock mode."""
        return self._config.get_current_ui_lock_mode(self.state.properties.get(REPORTED))

    def get_current_appliance_mode(self) -> str:
        """Return the current appliance mode."""
        return self._config.get_current_appliance_mode(self.state.properties.get(REPORTED))

    def get_current_hob_hood_window_notification(self) -> str:
        """Return the current Hob Hood window notification."""
        return self._config.get_current_hob_hood_window_notification(self.state.properties.get(REPORTED))

    def get_current_hob_hood_target_duration(self) -> int:
        """Return the current hob hood target duration."""
        return self._config.get_current_hob_hood_target_duration(self.state.properties.get(REPORTED))

    def get_current_zone_residual_heat_state(self, hob_zone: str) -> str:
        """Return the current zone residual heat state ."""
        return self._config.get_current_zone_residual_heat_state(hob_zone, self.state.properties.get(REPORTED))

    def get_current_zone_target_duration(self, hob_zone: str) -> int:
        """Return the current zone target duration."""
        return self._config.get_current_zone_target_duration(hob_zone, self.state.properties.get(REPORTED))

    def get_current_zone_reminder_time(self, hob_zone: str) -> int:
        """Return the current zone reminder time."""
        return self._config.get_current_zone_reminder_time(hob_zone, self.state.properties.get(REPORTED))

    def get_current_zone_hob_pot_detected(self, hob_zone: str) -> str:
        """Return the current zone hob pot detected."""
        return self._config.get_current_zone_hob_pot_detected(hob_zone, self.state.properties.get(REPORTED))

    def get_hood_fan_speed_command(self, fan_speed) -> dict[str, Any]:
        """Return the command payload to set a new hood fan speed."""
        return {
            self._config.get_property(HOB_HOOD): {
                self._config.get_property(HOOD_FAN_SPEED): fan_speed
            }
        }

    def get_hood_state_command(self, state) -> dict[str, Any]:
        """Return the command payload to set a new hood state."""
        return {
            self._config.get_property(HOB_HOOD): {
                self._config.get_property(HOOD_STATE): state
            }
        }

    def get_key_sound_tone_command(self, tone) -> dict[str, Any]:
        """Return the command payload to set the key sound tone."""
        return {
            self._config.get_property(KEY_SOUND_TONE): tone
        }

    def get_enable_child_lock_command(self) -> dict[str, Any]:
        """Return the command payload to enable the child lock. The child lock can be disabled only manually."""
        return {
            self._config.get_property(CHILD_LOCK): True
        }
