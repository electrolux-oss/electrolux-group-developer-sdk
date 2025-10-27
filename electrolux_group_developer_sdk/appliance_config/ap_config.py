"""Air Purifier configuration."""
from typing import Any
from ..feature_constants import *

from .config import ApplianceConfig
from ..constants import (
    FUJI,
    MUJU,
    PUREA9,
    VERBIER,
    WELLA5,
    WELLA7,
)
from ..constants import VALUES, MIN, MAX

# Configuration
AP_CONFIG = {
    MUJU: {
        WORKMODE: "Workmode",
        POWER_COMMAND: "Workmode",
        POWER_STATE: "Workmode",
        POWER_OFF_COMMAND: "PowerOff",
        WORKMODE_POWER_OFF: "PowerOff",
        POWER_ON_COMMAND: "Manual",
        FAN_SPEED: "Fanspeed",
        AIR_QUALITY: {
            PM_10: "PM10",
            PM_2_5: "PM2_5_approximate",
        },
        POWER_STATE_MAP: {
            "Manual": True,
            "Quiet": True,
            "Auto": True,
            "PowerOff": False,
        },
    },
    FUJI: {
        WORKMODE: "Workmode",
        POWER_COMMAND: "executeCommand",
        POWER_STATE: "applianceState",
        POWER_OFF_COMMAND: "off",
        POWER_ON_COMMAND: "on",
        WORKMODE_POWER_OFF: "PowerOff",
        FAN_SPEED: "Fanspeed",
        AIR_QUALITY: {
            PM_1: "PM1",
            PM_2_5: "PM2_5",
            PM_10: "PM10",
            TVOC: "TVOC",
        },
        POWER_STATE_MAP: {
            "running": True,
            "off": False,
            "monitoring": False,
            "alert": False,
        },
    },
    PUREA9: {
        WORKMODE: "Workmode",
        POWER_COMMAND: "Workmode",
        POWER_STATE: "Workmode",
        POWER_OFF_COMMAND: "PowerOff",
        POWER_ON_COMMAND: "Auto",
        WORKMODE_POWER_OFF: "PowerOff",
        FAN_SPEED: "Fanspeed",
        AIR_QUALITY: {
            PM_1: "PM1",
            PM_2_5: "PM2_5",
            PM_10: "PM10",
            TVOC: "TVOC",
        },
        POWER_STATE_MAP: {
            "Manual": True,
            "Quiet": True,
            "Auto": True,
            "PowerOff": False,
        },
    },
    VERBIER: {
        WORKMODE: "Workmode",
        POWER_COMMAND: "Workmode",
        POWER_STATE: "Workmode",
        POWER_OFF_COMMAND: "PowerOff",
        POWER_ON_COMMAND: "Auto",
        WORKMODE_POWER_OFF: "PowerOff",
        FAN_SPEED: "Fanspeed",
        AIR_QUALITY: {
            PM_1: "PM1",
            PM_2_5: "PM2_5",
            PM_10: "PM10",
            TVOC: "TVOC",
        },
        POWER_STATE_MAP: {
            "Manual": True,
            "Quiet": True,
            "Auto": True,
            "PowerOff": False,
        },
    },
    WELLA5: {
        WORKMODE: "Workmode",
        POWER_COMMAND: "Workmode",
        POWER_STATE: "Workmode",
        POWER_OFF_COMMAND: "PowerOff",
        POWER_ON_COMMAND: "Auto",
        WORKMODE_POWER_OFF: "PowerOff",
        FAN_SPEED: "Fanspeed",
        AIR_QUALITY: {
            PM_1: "PM1",
            PM_2_5: "PM2_5",
            PM_10: "PM10",
            TVOC: "TVOC",
        },
        POWER_STATE_MAP: {
            "Manual": True,
            "Quiet": True,
            "Auto": True,
            "PowerOff": False,
        },
    },
    WELLA7: {
        WORKMODE: "Workmode",
        POWER_COMMAND: "Workmode",
        POWER_STATE: "Workmode",
        POWER_OFF_COMMAND: "PowerOff",
        POWER_ON_COMMAND: "Auto",
        WORKMODE_POWER_OFF: "PowerOff",
        FAN_SPEED: "Fanspeed",
        AIR_QUALITY: {
            PM_1: "PM1",
            PM_2_5: "PM2_5",
            PM_10: "PM10",
            TVOC: "TVOC",
        },
        POWER_STATE_MAP: {
            "Manual": True,
            "Quiet": True,
            "Auto": True,
            "PowerOff": False,
        },
    },
}


class ApConfig(ApplianceConfig):
    """Config for AP devices."""

    def _get_power_state_map(self) -> dict[str, bool]:
        """Return the power state map."""
        return self.mapping.get(POWER_STATE_MAP)

    def get_air_quality_map(self) -> dict[str, str]:
        """Return the air quality map."""
        return self.mapping.get(AIR_QUALITY)

    def get_supported_modes(self) -> list[str]:
        """Get appliance modes."""
        key = self.get_property(WORKMODE)
        values = self.capabilities.get(key, {}).get(VALUES, {})
        return list(values.keys())

    def _get_fan_speed_capability(self) -> dict[str, Any]:
        """Get fan speed capability."""
        return self.capabilities.get(
            self.get_property(FAN_SPEED)
        )

    def get_min_fan_speed(self) -> int:
        """Get MIN fan speed."""
        return self._get_fan_speed_capability().get(MIN, 0)

    def get_max_fan_speed(self) -> int:
        """Get MAX fan speed."""
        return self._get_fan_speed_capability().get(MAX, 0)

    def get_current_mode(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current mode from the reported state."""
        return self._get_state(WORKMODE, reported_appliance_state)

    def get_current_fan_speed(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current fan speed from the reported state."""
        return self._get_state(FAN_SPEED, reported_appliance_state)

    def is_appliance_on(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Return true if the appliance is on."""
        power_state = self._get_state(POWER_STATE, reported_appliance_state)
        return self._get_power_state_map().get(power_state, False)

    def get_air_quality(self, reported_appliance_state: dict[str, Any], air_quality_property: str) -> float:
        """Get the air quality from the reported state."""
        return reported_appliance_state.get(self.get_air_quality_map().get(air_quality_property), 0)


class ApConfigManager:
    """Manager for AP device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in AP_CONFIG."""
        self._config = AP_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> ApConfig:
        """Return the appliance_config for a given model type."""

        return ApConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
