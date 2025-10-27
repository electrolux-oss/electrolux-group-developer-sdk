"""DAM Air conditioner configuration."""
from typing import Any

from .config import ApplianceConfig
from ..constants import VALUES, DAM_AC, PROPERTIES, CELSIUS, RANGE
from ..feature_constants import *

# Configuration
DAM_AC_CONFIG = {
    DAM_AC: {
        AIR_CONDITIONER: "airConditioner",
        TARGET_TEMPERATURE: "targetTemperature",
        FAN_MODE: "fanMode",
        MODE: "mode",
        AMBIENT_TEMPERATURE: "temperature",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState"
    }
}


class DamAcConfig(ApplianceConfig):
    """Config for DAM AC devices."""

    def _get_ac_nested_state(self, state_key: str, reported_appliance_state: dict[str, Any]) -> Any:
        """Return the state given a airConditioner nested specific key."""
        if not state_key:
            return None

        outer_value = reported_appliance_state.get(self.get_property(AIR_CONDITIONER))
        if not isinstance(outer_value, dict):
            return None

        return outer_value.get(self.get_property(state_key))

    def _get_air_conditioner_capabilities(self) -> dict[str, Any]:
        """Get air conditioner capabilities."""
        key = self.get_property(AIR_CONDITIONER)
        return self.capabilities.get(key, {}).get(PROPERTIES, {})

    def is_air_conditioner_capability_supported(self, feature: str) -> bool:
        """Return True if the appliance supports this ac capability."""
        key = self.get_property(feature)
        ac_capabilities = self._get_air_conditioner_capabilities()
        return key is not None and ac_capabilities is not None and key in ac_capabilities

    def get_supported_modes(self) -> list[str]:
        """Get appliance modes."""
        key = self.get_property(MODE)
        values = self._get_air_conditioner_capabilities().get(key, {}).get(VALUES, {})
        return list(values.keys())

    def get_supported_fan_speeds(self) -> list[str]:
        """Get appliance fan speeds."""
        key = self.get_property(FAN_MODE)
        values = self._get_air_conditioner_capabilities().get(key, {}).get(VALUES, {})
        return list(values.keys())

    def _get_target_temperature_capability(self) -> dict[str, Any]:
        """Get target temperature capability."""
        return self._get_air_conditioner_capabilities().get(
            self.get_property(TARGET_TEMPERATURE)
        )

    def get_supported_min_temp(self) -> float:
        """Get MIN temperature in Celsius."""
        return self._get_target_temperature_capability().get(RANGE)[0]

    def get_supported_max_temp(self) -> float:
        """Get MAX temperature in Celsius."""
        return self._get_target_temperature_capability().get(RANGE)[1]

    def get_supported_step_temp(self) -> float:
        """Get temperature STEP in Celsius."""
        return self._get_target_temperature_capability().get(RANGE)[2]

    def get_current_mode(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current mode from the reported state."""
        return self._get_ac_nested_state(MODE, reported_appliance_state)

    def get_current_temperature_unit(self) -> str:
        """Temperature unit for DAM AC is always Celsius."""
        return CELSIUS

    def get_current_target_temperature(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current target temperature from the reported state."""
        return self._get_ac_nested_state(TARGET_TEMPERATURE, reported_appliance_state)

    def get_current_ambient_temperature(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current ambient temperature from the reported state."""
        return self._get_state(AMBIENT_TEMPERATURE, reported_appliance_state)

    def get_current_appliance_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current appliance state from the reported state."""
        return self._get_ac_nested_state(APPLIANCE_STATE, reported_appliance_state)

    def get_current_fan_speed(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current fan speed from the reported state."""
        return self._get_ac_nested_state(FAN_MODE, reported_appliance_state)


class DamAcConfigManager:
    """Manager for DAM AC device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in DAM_AC_CONFIG."""
        self._config = DAM_AC_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> DamAcConfig:
        """Return the appliance_config for a given model type."""

        return DamAcConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
