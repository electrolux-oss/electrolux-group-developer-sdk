"""Hood configuration."""
from typing import Any

from .config import ApplianceConfig
from ..constants import VALUES, HB
from ..feature_constants import *

# Configuration
HB_CONFIG = {
    HB: {
        HOB_HOOD: "hobHood",
        HOOD_FAN_SPEED: "hobToHoodFanSpeed",
        HOOD_STATE: "hobToHoodState",
        KEY_SOUND_TONE: "keySoundTone",
        CHILD_LOCK: "childLock",
        APPLIANCE_STATE: "applianceState",
        ALERTS: "alerts",
        REMOTE_CONTROL: "remoteControl",
        UI_LOCK_MODE: "uiLockMode",
        APPLIANCE_MODE: "applianceMode",
        HOB_HOOD_TARGET_DURATION: "targetDuration",
        HOB_HOOD_WINDOW_NOTIFICATION: "windowNotification",
        ZONE_RESIDUAL_HEAT_STATE: "residualHeatState",
        ZONE_TARGET_DURATION: "targetDuration",
        ZONE_REMINDER_TIME: "reminderTime",
        ZONE_HOB_POT_DETECTED: "hobPotDetected",
        HOB_ZONE: "hobZone",
    }
}


class HbConfig(ApplianceConfig):
    """Config for HB devices."""

    def _get_nested_state(self, state_key: str, nested_state_key: str, reported_appliance_state: dict[str, Any]) -> Any:
        """Return the state given a nested specific key."""
        if not state_key or not nested_state_key:
            return None

        outer_value = reported_appliance_state.get(state_key)
        if not isinstance(outer_value, dict):
            return None

        return outer_value.get(nested_state_key)

    def is_hood_capability_supported(self, feature: str) -> bool:
        """Return True if the appliance supports this hobToHood capability."""
        key = self.get_property(feature)
        hood_capabilities = self.capabilities.get(self.get_property(HOB_HOOD), {})
        return key is not None and hood_capabilities is not None and key in hood_capabilities

    def is_hob_zone_capability_supported(self, zone: str, feature: str) -> bool:
        """Return True if the appliance supports this hob zone capability."""
        key = self.get_property(feature)
        hob_zone_capabilities = self.capabilities.get(zone)
        return key is not None and hob_zone_capabilities is not None and key in hob_zone_capabilities

    def get_supported_hood_fan_speed(self) -> list[str]:
        """Get supported hood fan speed."""
        values = self.capabilities.get(self.get_property(HOB_HOOD), {}).get(self.get_property(HOOD_FAN_SPEED), {}).get(
            VALUES, {})
        return [
            speed
            for speed, meta in values.items()
            if not meta.get("disabled", False)
        ]

    def get_supported_hood_state(self) -> list[str]:
        """Get supported hood state."""
        values = self.capabilities.get(self.get_property(HOB_HOOD), {}).get(self.get_property(HOOD_STATE), {}).get(
            VALUES, {})
        return [
            state
            for state, meta in values.items()
            if not meta.get("disabled", False)
        ]

    def get_supported_key_sound_tone(self) -> list[str]:
        """Get key sound tone."""
        values = self.capabilities.get(self.get_property(KEY_SOUND_TONE), {}).get(VALUES, {})
        return list(values.keys())

    def get_available_hob_zone(self, reported_appliance_state: dict[str, Any]) -> list[str]:
        """Get available hob zone from the state."""
        return [
            key
            for key, value in reported_appliance_state.items()
            if key.startswith(self.get_property(HOB_ZONE)) and isinstance(value, dict)
        ]

    def get_current_hood_fan_speed(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current hood fan speed from the reported state."""
        return self._get_nested_state(self.get_property(HOB_HOOD), self.get_property(HOOD_FAN_SPEED),
                                      reported_appliance_state)

    def get_current_hood_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current hood state from the reported state."""
        return self._get_nested_state(self.get_property(HOB_HOOD), self.get_property(HOOD_STATE),
                                      reported_appliance_state)

    def get_current_key_sound_tone(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current key sound tone from the reported state."""
        return self._get_state(KEY_SOUND_TONE, reported_appliance_state)

    def get_current_child_lock(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current child lock from the reported state."""
        return self._get_state(CHILD_LOCK, reported_appliance_state)

    def get_current_appliance_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current appliance state from the reported state."""
        return self._get_state(APPLIANCE_STATE, reported_appliance_state)

    def get_current_alerts(self, reported_appliance_state: dict[str, Any]) -> list[str]:
        """Get the current alerts from the reported state."""
        return self._get_state(ALERTS, reported_appliance_state)

    def get_current_remote_control(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current remote control from the reported state."""
        return self._get_state(REMOTE_CONTROL, reported_appliance_state)

    def get_current_ui_lock_mode(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current UI lock mode from the reported state."""
        return self._get_state(UI_LOCK_MODE, reported_appliance_state)

    def get_current_appliance_mode(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current appliance mode from the reported state."""
        return self._get_state(APPLIANCE_MODE, reported_appliance_state)

    def get_current_hob_hood_window_notification(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current Hob Hood window notification from the reported state."""
        return self._get_nested_state(self.get_property(HOB_HOOD), self.get_property(HOB_HOOD_WINDOW_NOTIFICATION),
                                      reported_appliance_state)

    def get_current_hob_hood_target_duration(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current hob hood target duration from the reported state."""
        return self._get_nested_state(self.get_property(HOB_HOOD), self.get_property(HOB_HOOD_TARGET_DURATION),
                                      reported_appliance_state)

    def get_current_zone_residual_heat_state(self, hob_zone: str, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current zone residual heat state from the reported state."""
        return self._get_nested_state(hob_zone, self.get_property(ZONE_RESIDUAL_HEAT_STATE), reported_appliance_state)

    def get_current_zone_target_duration(self, hob_zone: str, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current zone target duration from the reported state."""
        return self._get_nested_state(hob_zone, self.get_property(ZONE_TARGET_DURATION), reported_appliance_state)

    def get_current_zone_reminder_time(self, hob_zone: str, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current zone reminder time from the reported state."""
        return self._get_nested_state(hob_zone, self.get_property(ZONE_REMINDER_TIME), reported_appliance_state)

    def get_current_zone_hob_pot_detected(self, hob_zone: str, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current zone hob pot detected from the reported state."""
        return self._get_nested_state(hob_zone, self.get_property(ZONE_HOB_POT_DETECTED), reported_appliance_state)


class HbConfigManager:
    """Manager for HB device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in HB_CONFIG."""
        self._config = HB_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> HbConfig:
        """Return the appliance_config for a given model type."""

        return HbConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
