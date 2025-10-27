"""Combi Refrigerator configuration."""
from typing import Any

from .config import ApplianceConfig
from ..constants import VALUES, MIN, MAX, STEP, FAHRENHEIT, CR
from ..feature_constants import *

# cavities
FRIDGE = "fridge"
ICE_MAKER = "iceMaker"
FREEZER = "freezer"
EXTRA_CAVITY = "extraCavity"
CAVITIES = [FRIDGE, ICE_MAKER, EXTRA_CAVITY, FREEZER]

# Configuration
CR_CONFIG = {
    CR: {
        TARGET_TEMPERATURE_C: "targetTemperatureC",
        TARGET_TEMPERATURE_F: "targetTemperatureF",
        TEMPERATURE_REPRESENTATION: "temperatureRepresentation",
        APPLIANCE_STATE: "applianceState",
        ALERTS: "alerts",
        DOOR_STATE: "doorState",
        UI_LOCK_MODE: "uiLockMode",
        WATER_FILTER_STATE: "waterFilterState",
        AIR_FILTER_STATE: "airFilterState",
        DEFROST_TEMPERATURE_C: "defrostTemperatureC",  # iceMaker only
        DEFROST_TEMPERATURE_F: "defrostTemperatureF",  # iceMaker only
        VACATION_HOLIDAY_MODE: "vacationHolidayMode",
    },
}


class CrConfig(ApplianceConfig):
    """Config for CR devices."""

    def _get_nested_state(self, state_key: str, nested_state_key: str, reported_appliance_state: dict[str, Any]) -> Any:
        """Return the state given a nested specific key."""
        if not state_key or not nested_state_key:
            return None

        outer_value = reported_appliance_state.get(state_key)
        if not isinstance(outer_value, dict):
            return None

        return outer_value.get(nested_state_key)

    def is_cavity_capability_supported(self, cavity: str, feature) -> bool:
        """Return True if the appliance supports this cavity capability or any capability in a list."""
        cavity_capabilities = self.capabilities.get(cavity)
        if cavity_capabilities is None:
            return False

        if isinstance(feature, str):
            key = self.get_property(feature)
            return key is not None and key in cavity_capabilities
        elif isinstance(feature, list):
            for f in feature:
                key = self.get_property(f)
                if key is not None and key in cavity_capabilities:
                    return True
            return False
        return False

    def get_supported_cavities(self) -> list[str]:
        """Get supported cavities name from the capabilities."""
        return [key for key in CAVITIES if key in self.capabilities]

    def get_temperature_range(self, cavity: str, reported_appliance_state: dict) -> dict[str, float]:
        """Extract temperature range for the given program based on temperature unit."""
        current_unit = self.get_current_temperature_unit(reported_appliance_state)

        temperature_key = self.get_property(
            TARGET_TEMPERATURE_F) if (current_unit == FAHRENHEIT and self.get_property(
            TARGET_TEMPERATURE_F) in self.capabilities) else self.get_property(TARGET_TEMPERATURE_C)

        cavity_capabilities = self.capabilities.get(cavity)
        temperature_capability = cavity_capabilities.get(temperature_key)
        if all(k in temperature_capability and temperature_capability.get(k) is not None for k in (MIN, MAX, STEP)):
            return {
                MIN: temperature_capability.get(MIN),
                MAX: temperature_capability.get(MAX),
                STEP: temperature_capability.get(STEP),
            }
        return {
            MIN: 0,
            MAX: 0,
            STEP: 0,
        }

    def get_supported_extra_cavity_temperature(self, reported_appliance_state: dict) -> list[float]:
        """Extract the ExtraCavity supported temperature from the capabilities."""
        current_unit = self.get_current_temperature_unit(reported_appliance_state)
        temperature_key = self.get_property(
            TARGET_TEMPERATURE_F) if (current_unit == FAHRENHEIT and self.get_property(
            TARGET_TEMPERATURE_F) in self.capabilities) else self.get_property(TARGET_TEMPERATURE_C)

        extra_cavity_capabilities = self.capabilities.get(EXTRA_CAVITY)
        temperature_capability = extra_cavity_capabilities.get(temperature_key)
        return [float(temp) for temp in temperature_capability.get(VALUES, {}).keys()]

    def get_current_temperature_unit(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current temperature unit from the reported state."""
        return self._get_state(TEMPERATURE_REPRESENTATION, reported_appliance_state)

    def get_current_alerts(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current alerts from the reported state."""
        return self._get_state(ALERTS, reported_appliance_state)

    def get_current_ui_lock_mode(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current UI lock mode from the reported state."""
        return self._get_state(UI_LOCK_MODE, reported_appliance_state)

    def get_current_water_filter_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current water filter state from the reported state."""
        return self._get_state(WATER_FILTER_STATE, reported_appliance_state)

    def get_current_air_filter_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current air filter state from the reported state."""
        return self._get_state(AIR_FILTER_STATE, reported_appliance_state)

    def get_current_vacation_holiday_mode(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current vacation holiday mode from the reported state."""
        return self._get_state(VACATION_HOLIDAY_MODE, reported_appliance_state)

    def get_current_cavity_target_temperature_c(self, cavity: str, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current cavity target temperature C from the reported state."""
        return self._get_nested_state(cavity, self.get_property(TARGET_TEMPERATURE_C), reported_appliance_state)

    def get_current_cavity_target_temperature_f(self, cavity: str, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current cavity target temperature F from the reported state."""
        return self._get_nested_state(cavity, self.get_property(TARGET_TEMPERATURE_F), reported_appliance_state)

    def get_current_cavity_appliance_state(self, cavity: str, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current cavity appliance state from the reported state."""
        return self._get_nested_state(cavity, self.get_property(APPLIANCE_STATE), reported_appliance_state)

    def get_current_cavity_alerts(self, cavity: str, reported_appliance_state: dict[str, Any]) -> list[Any]:
        """Get the current cavity alerts from the reported state."""
        return self._get_nested_state(cavity, self.get_property(ALERTS), reported_appliance_state)

    def get_current_door_state(self, cavity: str, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current cavity door state from the reported state."""
        return self._get_nested_state(cavity, self.get_property(DOOR_STATE), reported_appliance_state)


class CrConfigManager:
    """Manager for CR device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in CR_CONFIG."""
        self._config = CR_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> CrConfig:
        """Return the appliance_config for a given model type."""
        return CrConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
