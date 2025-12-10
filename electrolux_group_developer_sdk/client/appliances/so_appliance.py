import datetime
from typing import Any, Optional

from pydantic import PrivateAttr

from .appliance_data import ApplianceData
from ...appliance_config.so_config import SoConfigManager, SoConfig, PROGRAM, TARGET_TEMPERATURE_C, \
    TARGET_TEMPERATURE_F, EXECUTE_COMMAND, TARGET_DURATION, CAVITY_LIGHT
from ...constants import REPORTED, MIN, MAX, STEP


class SOAppliance(ApplianceData):
    """
    Extended appliance data class for SO appliances.

    Adds access to capabilities and state via SoConfig.
    """
    _config: SoConfig = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        capabilities = self.details.capabilities if self.details else {}
        self._config = SoConfigManager().get_config(self.appliance.applianceType, capabilities)

    def is_feature_supported(self, feature: str | list[str]) -> bool:
        return self._config.is_capability_supported(feature)

    def is_cavity_feature_supported(self, cavity: str, feature) -> bool:
        return self._config.is_cavity_capability_supported(cavity, feature)

    def get_supported_cavities(self) -> list[str]:
        """Get supported cavities name from the capabilities."""
        return self._config.get_supported_cavities()

    def get_cavity_supported_programs(self, cavity: str) -> list[str]:
        """Return a list of cavity supported modes."""
        return self._config.get_cavity_supported_programs(cavity)

    def get_cavity_supported_min_temp(self, cavity: str, program: Optional[str] = None) -> float:
        """Return the minimum cavity supported temperature."""
        current_program = program if program is not None else self.get_current_cavity_program(cavity)
        return self._config.get_cavity_temperature_range(cavity, current_program,
                                                         self.state.properties.get(REPORTED)).get(MIN)

    def get_cavity_supported_max_temp(self, cavity: str, program: Optional[str] = None) -> float:
        """Return the maximum cavity supported temperature."""
        current_program = program if program is not None else self.get_current_cavity_program(cavity)
        return self._config.get_cavity_temperature_range(cavity, current_program,
                                                         self.state.properties.get(REPORTED)).get(MAX)

    def get_cavity_supported_step_temp(self, cavity: str, program: Optional[str] = None) -> float:
        """Return the cavity step increment for temperature control."""
        current_program = program if program is not None else self.get_current_cavity_program(cavity)
        return self._config.get_cavity_temperature_range(cavity, current_program,
                                                         self.state.properties.get(REPORTED)).get(STEP)

    def get_cavity_supported_min_duration(self, cavity: str, program: Optional[str] = None) -> float:
        """Return the minimum cavity supported timer duration."""
        current_program = program if program is not None else self.get_current_cavity_program(cavity)
        return self._config.get_cavity_timer_range(cavity, current_program).get(MIN)

    def get_cavity_supported_max_duration(self, cavity: str, program: Optional[str] = None) -> float:
        """Return the maximum cavity supported timer duration."""
        current_program = program if program is not None else self.get_current_cavity_program(cavity)
        return self._config.get_cavity_timer_range(cavity, current_program).get(MAX)

    def get_cavity_supported_step_duration(self, cavity: str, program: Optional[str] = None) -> float:
        """Return the cavity step increment for timer duration control."""
        current_program = program if program is not None else self.get_current_cavity_program(cavity)
        return self._config.get_cavity_timer_range(cavity, current_program).get(STEP)

    def get_current_cavity_program(self, cavity: str) -> str:
        """Return the current cavity program."""
        return self._config.get_current_cavity_program(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_target_temperature_c(self, cavity: str) -> float:
        """Return the current cavity target temperature in Celsius."""
        return self._config.get_current_cavity_target_temperature_c(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_target_temperature_f(self, cavity: str) -> float:
        """Return the current cavity target temperature in Fahrenheit."""
        return self._config.get_current_cavity_target_temperature_f(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_display_temperature_c(self, cavity: str) -> float:
        """Return the current cavity display temperature in Celsius."""
        return self._config.get_current_cavity_display_temperature_c(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_display_temperature_f(self, cavity: str) -> float:
        """Return the current cavity display temperature in Fahrenheit."""
        return self._config.get_current_cavity_display_temperature_f(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_appliance_state(self, cavity: str) -> str:
        """Return the current cavity appliance state."""
        return self._config.get_current_cavity_appliance_state(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_door_state(self, cavity: str) -> str:
        """Get the current cavity door state from the reported state."""
        return self._config.get_current_cavity_door_state(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_running_time(self, cavity: str) -> int:
        """Get the current cavity running time from the reported state."""
        return self._config.get_current_cavity_running_time(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_time_to_end(self, cavity: str) -> int:
        """Get the current cavity time to end from the reported state."""
        return self._config.get_current_cavity_time_to_end(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_target_duration(self, cavity: str) -> int:
        """Get the current cavity target duration from the reported state."""
        return self._config.get_current_cavity_target_duration(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_start_at(self, cavity: str) -> datetime:
        """Get the current cavity start at time from the reported state."""
        return self._config.get_current_cavity_start_at(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_cavity_light(self, cavity: str) -> bool:
        """Get the current cavity cavity light from the reported state."""
        return self._config.get_current_cavity_cavity_light(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_food_probe_insertion_state(self, cavity: str) -> str:
        """Get the current cavity food probe insertion state from the reported state."""
        return self._config.get_current_cavity_food_probe_insertion_state(cavity, self.state.properties.get(REPORTED))

    def get_current_cavity_display_food_probe_temperature_f(self, cavity: str) -> float:
        """Get the current cavity display food probe temperature f from the reported state."""
        return self._config.get_current_cavity_display_food_probe_temperature_f(cavity,
                                                                                self.state.properties.get(REPORTED))

    def get_current_cavity_display_food_probe_temperature_c(self, cavity: str) -> float:
        """Get the current cavity display food probe temperature c from the reported state."""
        return self._config.get_current_cavity_display_food_probe_temperature_c(cavity,
                                                                                self.state.properties.get(REPORTED))

    def get_current_remote_control(self) -> str:
        """Get the current remote control from the reported state."""
        return self._config.get_current_remote_control(self.state.properties.get(REPORTED))

    def get_current_alerts(self) -> list[Any]:
        """Get the current alerts from the reported state."""
        return self._config.get_current_alerts(self.state.properties.get(REPORTED))

    def get_current_temperature_unit(self) -> str:
        """Return the current temperature unit."""
        return self._config.get_current_temperature_unit(self.state.properties.get(REPORTED))

    def get_program_command(self, cavity: str, program: str) -> dict[str, Any]:
        """Return the command payload to set the cavity program."""
        return {cavity: {self._config.get_property(PROGRAM): program}}

    def get_cavity_light_command(self, cavity: str, on: bool) -> dict[str, Any]:
        """Return the command payload to set the cavity cavity light."""
        return {cavity: {self._config.get_property(CAVITY_LIGHT): on}}

    def get_temperature_c_command(self, cavity: str, temperature: float) -> dict[str, Any]:
        """Return the command payload to set the temperature in Celsius."""
        return {cavity: {self._config.get_property(TARGET_TEMPERATURE_C): temperature}}

    def get_temperature_f_command(self, cavity: str, temperature: float) -> dict[str, Any]:
        """Return the command payload to set the temperature in Fahrenheit."""
        return {cavity: {self._config.get_property(TARGET_TEMPERATURE_F): temperature}}

    def get_target_duration_command(self, cavity: str, duration_sec: int) -> dict[str, Any]:
        """Return the command payload to set the target duration."""
        return {cavity: {self._config.get_property(TARGET_DURATION): duration_sec}}

    def get_start_command(self, cavity: str) -> dict[str, Any]:
        """Return the command payload to turn the appliance ON."""
        return {cavity: {self._config.get_property(EXECUTE_COMMAND): "START"}}

    def get_stop_command(self, cavity: str) -> dict[str, Any]:
        """Return the command payload to turn the appliance OFF."""
        return {cavity: {self._config.get_property(EXECUTE_COMMAND): "STOPRESET"}}
