from typing import Any

from pydantic import PrivateAttr

from ...appliance_config.cr_config import CrConfig, CrConfigManager, TARGET_TEMPERATURE_F, TARGET_TEMPERATURE_C, \
    VACATION_HOLIDAY_MODE
from ...client.appliances.appliance_data import ApplianceData
from ...constants import REPORTED, MIN, MAX, STEP


class CRAppliance(ApplianceData):
    """
    Extended appliance data class for CR appliances.

    Adds access to capabilities and state via CrConfig.
    """
    _config: CrConfig = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        capabilities = self.details.capabilities if self.details else {}
        self._config = CrConfigManager().get_config(self.appliance.applianceType, capabilities)

    def is_feature_supported(self, feature) -> bool:
        return self._config.is_capability_supported(feature)

    def is_cavity_feature_supported(self, cavity: str, feature: str) -> bool:
        return self._config.is_cavity_capability_supported(cavity, feature)

    def get_supported_cavities(self) -> list[str]:
        """Get supported cavities name from the capabilities."""
        return self._config.get_supported_cavities()

    def get_supported_min_temperature(self, cavity: str) -> float:
        """Get min supported cavity temperature from the capabilities."""
        return self._config.get_temperature_range(cavity, self.state.properties.get(REPORTED)).get(MIN)

    def get_supported_max_temperature(self, cavity: str) -> float:
        """Get max supported cavity temperature from the capabilities."""
        return self._config.get_temperature_range(cavity, self.state.properties.get(REPORTED)).get(MAX)

    def get_supported_step_temperature(self, cavity: str) -> float:
        """Get step supported cavity temperature from the capabilities."""
        return self._config.get_temperature_range(cavity, self.state.properties.get(REPORTED)).get(STEP)

    def get_supported_extra_cavity_temperature(self) -> list[float]:
        """Get extra cavity supported temperature from the capabilities."""
        return self._config.get_supported_extra_cavity_temperature(self.state.properties.get(REPORTED))

    def get_current_temperature_unit(self) -> str:
        """Get the current temperature unit from the reported state."""
        return self._config.get_current_temperature_unit(self.state.properties.get(REPORTED))

    def get_current_alerts(self) -> str:
        """Get the current alerts from the reported state."""
        return self._config.get_current_alerts(self.state.properties.get(REPORTED))

    def get_current_ui_lock_mode(self) -> bool:
        """Get the current UI lock mode from the reported state."""
        return self._config.get_current_ui_lock_mode(self.state.properties.get(REPORTED))

    def get_current_water_filter_state(self) -> str:
        """Get the current water filter state from the reported state."""
        return self._config.get_current_water_filter_state(self.state.properties.get(REPORTED))

    def get_current_air_filter_state(self) -> str:
        """Get the current air filter state from the reported state."""
        return self._config.get_current_air_filter_state(self.state.properties.get(REPORTED))

    def get_current_vacation_holiday_mode(self) -> str:
        """Get the current vacation holiday mode from the reported state."""
        return self._config.get_current_vacation_holiday_mode(self.state.properties.get(REPORTED))

    def get_current_cavity_target_temperature_c(self, cavity: str) -> float:
        """Get the current cavity target temperature C from the reported state."""
        return self._config.get_current_cavity_target_temperature_c(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_target_temperature_f(self, cavity: str) -> float:
        """Get the current cavity target temperature F from the reported state."""
        return self._config.get_current_cavity_target_temperature_f(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_appliance_state(self, cavity: str) -> str:
        """Get the current cavity appliance state from the reported state."""
        return self._config.get_current_cavity_appliance_state(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_alerts(self, cavity: str) -> list[Any]:
        """Get the current cavity alerts from the reported state."""
        return self._config.get_current_cavity_alerts(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_door_state(self, cavity: str) -> str:
        """Get the current cavity door state from the reported state."""
        return self._config.get_current_door_state(cavity, self.state.properties.get(REPORTED))

    def get_set_cavity_temperature_f_command(self, cavity, temperature) -> dict[str, Any]:
        return {
            cavity: {self._config.get_property(TARGET_TEMPERATURE_F): temperature}
        }

    def get_set_cavity_temperature_c_command(self, cavity, temperature) -> dict[str, Any]:
        return {
            cavity: {self._config.get_property(TARGET_TEMPERATURE_C): temperature}
        }

    def get_set_vacation_holiday_mode_command(self, value) -> dict[str, Any]:
        return {self._config.get_property(VACATION_HOLIDAY_MODE): value}
