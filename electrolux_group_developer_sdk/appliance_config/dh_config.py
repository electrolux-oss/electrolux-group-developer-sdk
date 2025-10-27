"""Dehum configuration."""
from typing import Any

from .config import ApplianceConfig
from ..constants import DH, HUSKY, VALUES, MIN, MAX, STEP, APPLIANCE_STATE_RUNNING
from ..feature_constants import *

# Configuration
DH_CONFIG = {
    DH: {
        MODE: "mode",
        TARGET_HUMIDITY: "targetHumidity",
        SENSOR_HUMIDITY: "sensorHumidity",
        FAN_SPEED: "fanSpeedSetting",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState",
        EXECUTE_COMMAND_OFF: "OFF",
        EXECUTE_COMMAND_ON: "ON",
        MODE_OFF: "OFF"
    },
    HUSKY: {
        MODE: "mode",
        TARGET_HUMIDITY: "targetHumidity",
        SENSOR_HUMIDITY: "sensorHumidity",
        FAN_SPEED: "fanSpeedSetting",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState",
        EXECUTE_COMMAND_OFF: "OFF",
        EXECUTE_COMMAND_ON: "ON",
        MODE_OFF: "OFF"
    },
}


class DhConfig(ApplianceConfig):
    """Config for DH devices."""

    def get_supported_modes(self) -> list[str]:
        """Get appliance modes."""
        key = self.get_property(MODE)
        values = self.capabilities.get(key, {}).get(VALUES, {})
        return list(values.keys())

    def get_supported_fan_speeds(self) -> list[str]:
        """Get appliance fan speeds."""
        key = self.get_property(FAN_SPEED)
        values = self.capabilities.get(key, {}).get(VALUES, {})
        return list(values.keys())

    def _get_target_humidity_capability(self) -> dict[str, Any]:
        """Get target humidity capability."""
        return self.capabilities.get(
            self.get_property(TARGET_HUMIDITY)
        )

    def get_supported_min_humidity(self) -> float:
        """Get MIN target humidity."""
        return self._get_target_humidity_capability().get(MIN)

    def get_supported_max_humidity(self) -> float:
        """Get MAX target humidity."""
        return self._get_target_humidity_capability().get(MAX)

    def get_supported_step_humidity(self) -> float:
        """Get humidity STEP."""
        return self._get_target_humidity_capability().get(STEP)

    def get_current_mode(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current mode from the reported state."""
        return self._get_state(MODE, reported_appliance_state)

    def get_current_sensor_humidity(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current sensor humidity from the reported state."""
        return self._get_state(SENSOR_HUMIDITY, reported_appliance_state)

    def get_current_target_humidity(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current target humidity from the reported state."""
        return self._get_state(TARGET_HUMIDITY, reported_appliance_state)

    def is_appliance_on(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current appliance state from the reported state."""
        appliance_state = self.get_current_appliance_state(reported_appliance_state)
        return appliance_state == APPLIANCE_STATE_RUNNING

    def get_current_appliance_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current appliance state from the reported state."""
        return self._get_state(APPLIANCE_STATE, reported_appliance_state)

    def get_current_fan_speed(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current fan speed from the reported state."""
        return self._get_state(FAN_SPEED, reported_appliance_state)


class DhConfigManager:
    """Manager for DH device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in DH_CONFIG."""
        self._config = DH_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> DhConfig:
        """Return the appliance_config for a given model type."""

        return DhConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
