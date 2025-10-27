"""Air conditioner configuration."""
from typing import Any

from .config import ApplianceConfig
from ..constants import VALUES, MAX, MIN, FAHRENHEIT, STEP, AC, CA, AZUL, BOGONG, PANTHER, TELICA
from ..feature_constants import *

# Configuration
AC_CONFIG = {
    AC: {
        TARGET_TEMPERATURE_C: "targetTemperatureC",
        TARGET_TEMPERATURE_F: "targetTemperatureF",
        FAN_SPEED_SETTING: "fanSpeedSetting",
        MODE: "mode",
        AMBIENT_TEMPERATURE_C: "ambientTemperatureC",
        AMBIENT_TEMPERATURE_F: "ambientTemperatureF",
        TEMPERATURE_REPRESENTATION: "temperatureRepresentation",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState"
    },
    CA: {
        TARGET_TEMPERATURE_C: "targetTemperatureC",
        TARGET_TEMPERATURE_F: "targetTemperatureF",
        FAN_SPEED_SETTING: "fanSpeedSetting",
        MODE: "mode",
        AMBIENT_TEMPERATURE_C: "ambientTemperatureC",
        AMBIENT_TEMPERATURE_F: "ambientTemperatureF",
        TEMPERATURE_REPRESENTATION: "temperatureRepresentation",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState"
    },
    AZUL: {
        TARGET_TEMPERATURE_C: "targetTemperatureC",
        TARGET_TEMPERATURE_F: "targetTemperatureF",
        FAN_SPEED_SETTING: "fanSpeedSetting",
        MODE: "mode",
        AMBIENT_TEMPERATURE_C: "ambientTemperatureC",
        AMBIENT_TEMPERATURE_F: "ambientTemperatureF",
        TEMPERATURE_REPRESENTATION: "temperatureRepresentation",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState"
    },
    BOGONG: {
        TARGET_TEMPERATURE_C: "targetTemperatureC",
        TARGET_TEMPERATURE_F: "targetTemperatureF",
        FAN_SPEED_SETTING: "fanSpeedSetting",
        MODE: "mode",
        AMBIENT_TEMPERATURE_C: "ambientTemperatureC",
        AMBIENT_TEMPERATURE_F: "ambientTemperatureF",
        TEMPERATURE_REPRESENTATION: "temperatureRepresentation",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState"
    },
    PANTHER: {
        TARGET_TEMPERATURE_C: "targetTemperatureC",
        TARGET_TEMPERATURE_F: "targetTemperatureF",
        FAN_SPEED_SETTING: "fanSpeedSetting",
        MODE: "mode",
        AMBIENT_TEMPERATURE_C: "ambientTemperatureC",
        AMBIENT_TEMPERATURE_F: "ambientTemperatureF",
        TEMPERATURE_REPRESENTATION: "temperatureRepresentation",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState"
    },
    TELICA: {
        TARGET_TEMPERATURE_C: "targetTemperatureC",
        TARGET_TEMPERATURE_F: "targetTemperatureF",
        FAN_SPEED_SETTING: "fanSpeedSetting",
        MODE: "mode",
        AMBIENT_TEMPERATURE_C: "ambientTemperatureC",
        AMBIENT_TEMPERATURE_F: "ambientTemperatureF",
        TEMPERATURE_REPRESENTATION: "temperatureRepresentation",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState"
    }
}


class AcConfig(ApplianceConfig):
    """Config for AC devices."""

    def get_supported_modes(self) -> list[str]:
        """Get appliance modes."""
        key = self.get_property(MODE)
        values = self.capabilities.get(key, {}).get(VALUES, {})
        return list(values.keys())

    def get_supported_fan_speeds(self) -> list[str]:
        """Get appliance fan speeds."""
        key = self.get_property(FAN_SPEED_SETTING)
        values = self.capabilities.get(key, {}).get(VALUES, {})
        return list(values.keys())

    def _get_target_temperature_f_capability(self) -> dict[str, Any]:
        """Get target temperature F capability."""
        return self.capabilities.get(
            self.get_property(TARGET_TEMPERATURE_F)
        )

    def _get_target_temperature_c_capability(self) -> dict[str, Any]:
        """Get target temperature C capability."""
        return self.capabilities.get(
            self.get_property(TARGET_TEMPERATURE_C)
        )

    def get_supported_min_temp(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get MIN temperature based on the current unit. The default is CELSIUS."""
        if self.get_current_temperature_unit(reported_appliance_state) == FAHRENHEIT:
            return self._get_target_temperature_f_capability().get(MIN)
        return self._get_target_temperature_c_capability().get(MIN)

    def get_supported_max_temp(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get MAX temperature based on the current unit. The default is CELSIUS."""
        if self.get_current_temperature_unit(reported_appliance_state) == FAHRENHEIT:
            return self._get_target_temperature_f_capability().get(MAX)
        return self._get_target_temperature_c_capability().get(MAX)

    def get_supported_step_temp(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get temperature STEP based on the current unit. The default is CELSIUS."""
        if self.get_current_temperature_unit(reported_appliance_state) == FAHRENHEIT:
            return self._get_target_temperature_f_capability().get(STEP)
        return self._get_target_temperature_c_capability().get(STEP)

    def get_current_mode(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current mode from the reported state."""
        return self._get_state(MODE, reported_appliance_state)

    def get_current_temperature_unit(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current temperature unit from the reported state."""
        return self._get_state(TEMPERATURE_REPRESENTATION, reported_appliance_state)

    def get_current_target_temperature_c(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current target temperature C from the reported state."""
        return self._get_state(TARGET_TEMPERATURE_C, reported_appliance_state)

    def get_current_target_temperature_f(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current target temperature F from the reported state."""
        return self._get_state(TARGET_TEMPERATURE_F, reported_appliance_state)

    def get_current_ambient_temperature_c(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current ambient temperature C from the reported state."""
        return self._get_state(AMBIENT_TEMPERATURE_C, reported_appliance_state)

    def get_current_ambient_temperature_f(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current ambient temperature F from the reported state."""
        return self._get_state(AMBIENT_TEMPERATURE_F, reported_appliance_state)

    def get_current_appliance_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current appliance state from the reported state."""
        return self._get_state(APPLIANCE_STATE, reported_appliance_state)

    def get_current_fan_speed(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current fan speed from the reported state."""
        return self._get_state(FAN_SPEED_SETTING, reported_appliance_state)


class AcConfigManager:
    """Manager for AC device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in AC_CONFIG."""
        self._config = AC_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> AcConfig:
        """Return the appliance_config for a given model type."""

        return AcConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
