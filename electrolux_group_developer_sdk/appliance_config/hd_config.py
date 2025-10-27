"""HOOD configuration."""
from typing import Any

from .config import ApplianceConfig
from ..constants import VALUES, MIN, MAX, STEP, HD
from ..feature_constants import *

# Configuration
HD_CONFIG = {
    HD: {
        HOOD_FAN_LEVEL: "hoodFanLevel",
        LIGHT_INTENSITY: "lightIntensity",
        LIGHT_COLOR_TEMPERATURE: "lightColorTemperature",
        HOOD_CHARC_FILTER_TIME: "hoodCharcFilterTimer",
        HOOD_FILTER_CHARC_ENABLE: "hoodFilterCharcEnable",
        HUMAN_CENTRIC_LIGHT_EVENT_STATE: "humanCentricLightEventState",
        APPLIANCE_MODE: "applianceMode",
        APPLIANCE_STATE: "applianceState",
        DRAWER_STATUS: "drawerStatus",
        REMOTE_CONTROL: "remoteControl",
        ALERTS: "alerts",
        HOOD_GREASE_FILTER_TIMER: "hoodGreaseFilterTimer",
        SOUND_VOLUME: "soundVolume",
        TARGET_DURATION: "targetDuration",
        TVOC_FILTER_TIME: "tvocFilterTime",
        HOOD_AUTO_SWITCH_OFF_EVENT: "hoodAutoSwitchOffEvent"
    },
}


class HdConfig(ApplianceConfig):
    """Config for HD devices."""

    def get_supported_hood_fan_level(self) -> list[str]:
        """Get appliance hood fan level."""
        key = self.get_property(HOOD_FAN_LEVEL)
        values = self.capabilities.get(key, {}).get(VALUES, {})
        return [
            program
            for program, meta in values.items()
        ]

    def get_light_intensity_range(self) -> dict[str, int]:
        """Get light intensity range."""
        capability = self.capabilities.get(self.get_property(LIGHT_INTENSITY), {})

        return {
            MIN: capability.get(MIN),
            MAX: capability.get(MAX),
            STEP: capability.get(STEP),
        }

    def get_light_color_temperature_range(self) -> dict[str, int]:
        """Get light color temperature range."""
        capability = self.capabilities.get(self.get_property(LIGHT_COLOR_TEMPERATURE), {})

        return {
            MIN: capability.get(MIN),
            MAX: capability.get(MAX),
            STEP: capability.get(STEP),
        }

    def get_current_hood_fan_level(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current hood fan level from the reported state."""
        return reported_appliance_state.get(self.get_property(HOOD_FAN_LEVEL))

    def get_current_light_intensity(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current light intensity from the reported state."""
        return reported_appliance_state.get(self.get_property(LIGHT_INTENSITY))

    def get_current_light_color_temperature(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current light color temperature from the reported state."""
        return reported_appliance_state.get(self.get_property(LIGHT_COLOR_TEMPERATURE))

    def get_current_hood_charc_filter_timer(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current hood charc filter timer from the reported state."""
        return reported_appliance_state.get(self.get_property(HOOD_CHARC_FILTER_TIME))

    def get_current_hood_filter_charc_enable(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current hood filter charc enable from the reported state."""
        return reported_appliance_state.get(self.get_property(HOOD_FILTER_CHARC_ENABLE))

    def get_current_human_centric_light_event_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current human centric light event state from the reported state."""
        return reported_appliance_state.get(self.get_property(HUMAN_CENTRIC_LIGHT_EVENT_STATE))

    def get_current_appliance_mode(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current appliance mode from the reported state."""
        return reported_appliance_state.get(self.get_property(APPLIANCE_MODE))

    def get_current_drawer_status(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current drawer status from the reported state."""
        return reported_appliance_state.get(self.get_property(DRAWER_STATUS))

    def get_current_hood_grease_filter_time(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current hood grease filter time from the reported state."""
        return reported_appliance_state.get(self.get_property(HOOD_GREASE_FILTER_TIMER))

    def get_current_sound_volume(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current sound volume from the reported state."""
        return reported_appliance_state.get(self.get_property(SOUND_VOLUME))

    def get_current_tvoc_filter_time(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current tvoc filter time from the reported state."""
        return reported_appliance_state.get(self.get_property(TVOC_FILTER_TIME))

    def get_current_hood_auto_switch_off_event(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current hood auto switch off event from the reported state."""
        return reported_appliance_state.get(self.get_property(HOOD_AUTO_SWITCH_OFF_EVENT))

    def get_current_appliance_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current appliance state from the reported state."""
        return self._get_state(APPLIANCE_STATE, reported_appliance_state)

    def get_current_target_duration(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current target duration from the reported state."""
        return self._get_state(TARGET_DURATION, reported_appliance_state)

    def get_current_alerts(self, reported_appliance_state: dict[str, Any]) -> list[Any]:
        """Get the current alerts from the reported state."""
        return self._get_state(ALERTS, reported_appliance_state)

    def get_current_remote_control(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current remote control from the reported state."""
        return self._get_state(REMOTE_CONTROL, reported_appliance_state)


class HdConfigManager:
    """Manager for HD device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in HD_CONFIG."""
        self._config = HD_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> HdConfig:
        """Return the appliance_config for a given model type."""
        return HdConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
