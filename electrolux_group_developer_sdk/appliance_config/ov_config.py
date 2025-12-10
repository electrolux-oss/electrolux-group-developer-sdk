"""Oven configuration."""
import datetime
from typing import Any, Optional
from zoneinfo import ZoneInfo

from .config import ApplianceConfig
from ..constants import VALUES, OV, APPLIANCE_STATE_DELAYED_START, MIN, MAX, STEP, DISABLED, FAHRENHEIT
from ..feature_constants import *

# Constants
DEFAULT_MIN_C_TEMP = 0.0
DEFAULT_MAX_C_TEMP = 350.0
DEFAULT_MIN_F_TEMP = 100.0
DEFAULT_MAX_F_TEMP = 550.0
DEFAULT_STEP_TEMP = 5.0

DEFAULT_MIN_DURATION = 0
DEFAULT_MAX_DURATION = 86340
DEFAULT_STEP_DURATION = 60

# Configuration
OV_CONFIG = {
    OV: {
        TARGET_TEMPERATURE_C: "targetTemperatureC",
        TARGET_TEMPERATURE_F: "targetTemperatureF",
        PROGRAM: "program",
        DISPLAY_TEMPERATURE_C: "displayTemperatureC",
        DISPLAY_TEMPERATURE_F: "displayTemperatureF",
        TEMPERATURE_REPRESENTATION: "temperatureRepresentation",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState",
        REMOTE_CONTROL: "remoteControl",
        ALERTS: "alerts",
        DOOR_STATE: "doorState",
        TIME_TO_END: "timeToEnd",
        TARGET_DURATION: "targetDuration",
        START_TIME: "startTime",
        RUNNING_TIME: "runningTime",
        FOOD_PROBE_STATE: "foodProbeInsertionState",
        DISPLAY_FOOD_PROBE_TEMPERATURE_C: "displayFoodProbeTemperatureC",
        DISPLAY_FOOD_PROBE_TEMPERATURE_F: "displayFoodProbeTemperatureF",
        CAVITY_LIGHT: "cavityLight"
    },
}


class OvConfig(ApplianceConfig):
    """Config for OV devices."""

    def get_supported_programs(self) -> list[str]:
        """Get appliance programs."""
        key = self.get_property(PROGRAM)
        values = self.capabilities.get(key, {}).get(VALUES, {})
        return [
            program
            for program, meta in values.items()
            if not meta.get("disabled", False)
        ]

    def get_temperature_range(self, program_name: str, reported_appliance_state: dict[str, Any]) -> dict[str, float]:
        """Extract temperature range for the given program based on temperature unit."""

        program_trigger = self.capabilities.get(self.get_property(PROGRAM), {}).get(VALUES, {}).get(program_name, {})
        current_unit = self.get_current_temperature_unit(reported_appliance_state)

        temperature_key = self.get_property(
            TARGET_TEMPERATURE_F) if current_unit == FAHRENHEIT else self.get_property(TARGET_TEMPERATURE_C)

        temp_config = program_trigger.get(temperature_key)

        if temp_config and temp_config.get(DISABLED, False):
            return {
                MIN: 0.0,
                MAX: 0.0,
                STEP: 0.0,
            }

        if temp_config:
            return {
                MIN: float(temp_config.get(MIN)),
                MAX: float(temp_config.get(MAX)),
                STEP: float(temp_config.get(STEP)),
            }

        temperature_capability = self.capabilities.get(temperature_key)
        if all(k in temperature_capability and temperature_capability.get(k) is not None for k in (MIN, MAX, STEP)):
            return {
                MIN: temperature_capability.get(MIN),
                MAX: temperature_capability.get(MAX),
                STEP: temperature_capability.get(STEP),
            }

        return {
            MIN: DEFAULT_MIN_F_TEMP,
            MAX: DEFAULT_MAX_F_TEMP,
            STEP: DEFAULT_STEP_TEMP,
        } if current_unit == FAHRENHEIT else {
            MIN: DEFAULT_MIN_C_TEMP,
            MAX: DEFAULT_MAX_C_TEMP,
            STEP: DEFAULT_STEP_TEMP,
        }

    def get_timer_range(self, program_name: str) -> dict[str, int]:
        """Extract timer range for the given program."""

        program_trigger = self.capabilities.get(self.get_property(PROGRAM), {}).get(VALUES, {}).get(program_name, {})

        duration_config = program_trigger.get(self.get_property(TARGET_DURATION))
        if duration_config and duration_config.get(DISABLED, False):
            return {
                MIN: 0,
                MAX: 0,
                STEP: 0,
            }

        if duration_config:
            return {
                MIN: duration_config.get(MIN),
                MAX: duration_config.get(MAX),
                STEP: duration_config.get(STEP),
            }

        duration_capability = self.capabilities.get(self.get_property(TARGET_DURATION))
        if all(k in duration_capability and duration_capability.get(k) is not None for k in (MIN, MAX, STEP)):
            return {
                MIN: duration_capability.get(MIN),
                MAX: duration_capability.get(MAX),
                STEP: duration_capability.get(STEP),
            }

        return {
            MIN: DEFAULT_MIN_DURATION,
            MAX: DEFAULT_MAX_DURATION,
            STEP: DEFAULT_STEP_DURATION,
        }

    def get_current_program(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current program from the reported state."""
        return reported_appliance_state.get(self.get_property(PROGRAM))

    def get_current_temperature_unit(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current temperature unit from the reported state."""
        return self._get_state(TEMPERATURE_REPRESENTATION, reported_appliance_state)

    def get_current_target_temperature_c(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current target temperature C from the reported state."""
        return self._get_state(TARGET_TEMPERATURE_C, reported_appliance_state)

    def get_current_target_temperature_f(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current target temperature F from the reported state."""
        return self._get_state(TARGET_TEMPERATURE_F, reported_appliance_state)

    def get_current_display_temperature_c(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current display temperature C from the reported state."""
        return self._get_state(DISPLAY_TEMPERATURE_C, reported_appliance_state)

    def get_current_display_temperature_f(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current display temperature F from the reported state."""
        return self._get_state(DISPLAY_TEMPERATURE_F, reported_appliance_state)

    def get_current_appliance_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current appliance state from the reported state."""
        return self._get_state(APPLIANCE_STATE, reported_appliance_state)

    def get_current_time_to_end(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current time to end from the reported state."""
        return self._get_state(TIME_TO_END, reported_appliance_state)

    def get_current_target_duration(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current target duration from the reported state."""
        return self._get_state(TARGET_DURATION, reported_appliance_state)

    def get_current_alerts(self, reported_appliance_state: dict[str, Any]) -> list[Any]:
        """Get the current alerts from the reported state."""
        return self._get_state(ALERTS, reported_appliance_state)

    def get_current_remote_control(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current remote control from the reported state."""
        return self._get_state(REMOTE_CONTROL, reported_appliance_state)

    def get_current_door_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current door state from the reported state."""
        return self._get_state(DOOR_STATE, reported_appliance_state)

    def get_current_running_time(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current running time from the reported state."""
        return self._get_state(RUNNING_TIME, reported_appliance_state)

    def get_current_cavity_light(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current cavity light from the reported state."""
        return self._get_state(CAVITY_LIGHT, reported_appliance_state)

    def get_current_food_probe_insertion_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current food probe insertion state from the reported state."""
        return self._get_state(FOOD_PROBE_STATE, reported_appliance_state)

    def get_current_display_food_probe_temperature_f(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current display food probe temperature f from the reported state."""
        return self._get_state(DISPLAY_FOOD_PROBE_TEMPERATURE_F, reported_appliance_state)

    def get_current_display_food_probe_temperature_c(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current display food probe temperature c from the reported state."""
        return self._get_state(DISPLAY_FOOD_PROBE_TEMPERATURE_C, reported_appliance_state)

    def get_current_start_at(self, reported_appliance_state: dict[str, Any]) -> Optional[datetime.datetime]:
        """Get the current start at time from the reported state."""
        appliance_state = self.get_current_appliance_state(reported_appliance_state)

        if appliance_state != APPLIANCE_STATE_DELAYED_START:
            return None

        now = datetime.datetime.now(ZoneInfo("UTC"))
        start_time = self._get_state(START_TIME, reported_appliance_state)

        if start_time is not None and start_time not in (-1, 0):
            return now + datetime.timedelta(seconds=start_time)

        return None


class OvConfigManager:
    """Manager for OV device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in OV_CONFIG."""
        self._config = OV_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> OvConfig:
        """Return the appliance_config for a given model type."""
        return OvConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
