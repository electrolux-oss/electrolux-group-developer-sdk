import datetime
from typing import Any, Optional

from pydantic import PrivateAttr

from .appliance_data import ApplianceData
from ...appliance_config.ov_config import OvConfig, OvConfigManager, PROGRAM, TARGET_TEMPERATURE_C, \
    TARGET_TEMPERATURE_F, EXECUTE_COMMAND, TARGET_DURATION, CAVITY_LIGHT
from ...constants import REPORTED, MIN, MAX, STEP


class OVAppliance(ApplianceData):
    """
    Extended appliance data class for OV appliances.

    Adds access to capabilities and state via OvConfig.
    """
    _config: OvConfig = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        capabilities = self.details.capabilities if self.details else {}
        self._config = OvConfigManager().get_config(self.appliance.applianceType, capabilities)

    def is_feature_supported(self, feature: str | list[str]) -> bool:
        return self._config.is_capability_supported(feature)

    def get_supported_programs(self) -> list[str]:
        """Return a list of supported modes."""
        return self._config.get_supported_programs()

    def get_supported_min_temp(self, program: Optional[str] = None) -> float:
        """Return the minimum supported temperature."""
        current_program = program if program is not None else self.get_current_program()
        return self._config.get_temperature_range(current_program, self.state.properties.get(REPORTED)).get(MIN)

    def get_supported_max_temp(self, program: Optional[str] = None) -> float:
        """Return the maximum supported temperature."""
        current_program = program if program is not None else self.get_current_program()
        return self._config.get_temperature_range(current_program, self.state.properties.get(REPORTED)).get(MAX)

    def get_supported_step_temp(self, program: Optional[str] = None) -> float:
        """Return the step increment for temperature control."""
        current_program = program if program is not None else self.get_current_program()
        return self._config.get_temperature_range(current_program, self.state.properties.get(REPORTED)).get(STEP)

    def get_supported_min_duration(self, program: Optional[str] = None) -> float:
        """Return the minimum supported timer duration."""
        current_program = program if program is not None else self.get_current_program()
        return self._config.get_timer_range(current_program).get(MIN)

    def get_supported_max_duration(self, program: Optional[str] = None) -> float:
        """Return the maximum supported timer duration."""
        current_program = program if program is not None else self.get_current_program()
        return self._config.get_timer_range(current_program).get(MAX)

    def get_supported_step_duration(self, program: Optional[str] = None) -> float:
        """Return the step increment for timer duration control."""
        current_program = program if program is not None else self.get_current_program()
        return self._config.get_timer_range(current_program).get(STEP)

    def get_current_program(self) -> str:
        """Return the current program."""
        return self._config.get_current_program(self.state.properties.get(REPORTED))

    def get_current_temperature_unit(self) -> str:
        """Return the current temperature unit."""
        return self._config.get_current_temperature_unit(self.state.properties.get(REPORTED))

    def get_current_target_temperature_c(self) -> float:
        """Return the current target temperature in Celsius."""
        return self._config.get_current_target_temperature_c(self.state.properties.get(REPORTED))

    def get_current_target_temperature_f(self) -> float:
        """Return the current target temperature in Fahrenheit."""
        return self._config.get_current_target_temperature_f(self.state.properties.get(REPORTED))

    def get_current_display_temperature_c(self) -> float:
        """Return the current display temperature in Celsius."""
        return self._config.get_current_display_temperature_c(self.state.properties.get(REPORTED))

    def get_current_display_temperature_f(self) -> float:
        """Return the current display temperature in Fahrenheit."""
        return self._config.get_current_display_temperature_f(self.state.properties.get(REPORTED))

    def get_current_appliance_state(self) -> str:
        """Return the current appliance state."""
        return self._config.get_current_appliance_state(self.state.properties.get(REPORTED))

    def get_current_door_state(self) -> str:
        """Get the current door state from the reported state."""
        return self._config.get_current_door_state(self.state.properties.get(REPORTED))

    def get_current_remote_control(self) -> str:
        """Get the current remote control from the reported state."""
        return self._config.get_current_remote_control(self.state.properties.get(REPORTED))

    def get_current_alerts(self) -> list[Any]:
        """Get the current alerts from the reported state."""
        return self._config.get_current_alerts(self.state.properties.get(REPORTED))

    def get_current_running_time(self) -> int:
        """Get the current running time from the reported state."""
        return self._config.get_current_running_time(self.state.properties.get(REPORTED))

    def get_current_time_to_end(self) -> int:
        """Get the current time to end from the reported state."""
        return self._config.get_current_time_to_end(self.state.properties.get(REPORTED))

    def get_current_target_duration(self) -> int:
        """Get the current target duration from the reported state."""
        return self._config.get_current_target_duration(self.state.properties.get(REPORTED))

    def get_current_start_at(self) -> datetime:
        """Get the current start at time from the reported state."""
        return self._config.get_current_start_at(self.state.properties.get(REPORTED))

    def get_current_cavity_light(self) -> bool:
        """Get the current cavity light from the reported state."""
        return self._config.get_current_cavity_light(self.state.properties.get(REPORTED))

    def get_current_food_probe_insertion_state(self) -> str:
        """Get the current food probe insertion state from the reported state."""
        return self._config.get_current_food_probe_insertion_state(self.state.properties.get(REPORTED))

    def get_current_display_food_probe_temperature_f(self) -> float:
        """Get the current display food probe temperature f from the reported state."""
        return self._config.get_current_display_food_probe_temperature_f(self.state.properties.get(REPORTED))

    def get_current_display_food_probe_temperature_c(self) -> float:
        """Get the current display food probe temperature c from the reported state."""
        return self._config.get_current_display_food_probe_temperature_c(self.state.properties.get(REPORTED))

    def get_program_command(self, program: str) -> dict[str, Any]:
        """Return the command payload to set the program."""
        return {
            self._config.get_property(PROGRAM): program
        }

    def get_cavity_light_command(self, on: bool) -> dict[str, Any]:
        """Return the command payload to set the cavity light."""
        return {
            self._config.get_property(CAVITY_LIGHT): on
        }

    def get_temperature_c_command(self, temperature: float) -> dict[str, Any]:
        """Return the command payload to set the temperature in Celsius."""
        return {
            self._config.get_property(TARGET_TEMPERATURE_C): temperature
        }

    def get_temperature_f_command(self, temperature: float) -> dict[str, Any]:
        """Return the command payload to set the temperature in Fahrenheit."""
        return {
            self._config.get_property(TARGET_TEMPERATURE_F): temperature
        }

    def get_target_duration_command(self, duration_sec: int) -> dict[str, Any]:
        """Return the command payload to set the target duration."""
        return {
            self._config.get_property(TARGET_DURATION): duration_sec
        }

    def get_start_command(self) -> dict[str, Any]:
        """Return the command payload to turn the appliance ON."""
        return {
            self._config.get_property(EXECUTE_COMMAND): "START"
        }

    def get_stop_command(self) -> dict[str, Any]:
        """Return the command payload to turn the appliance OFF."""
        return {
            self._config.get_property(EXECUTE_COMMAND): "STOPRESET"
        }
