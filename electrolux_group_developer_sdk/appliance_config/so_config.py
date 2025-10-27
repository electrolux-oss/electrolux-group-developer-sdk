"""Structured Oven configuration."""
import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .config import ApplianceConfig
from ..constants import VALUES, SO, APPLIANCE_STATE_DELAYED_START, MIN, MAX, STEP, DISABLED, FAHRENHEIT
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

UPPER_OVEN = "upperOven"
BOTTOM_OVEN = "bottomOven"
CAVITIES = [BOTTOM_OVEN, UPPER_OVEN]

# Configuration
SO_CONFIG = {
    SO: {
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


class SoConfig(ApplianceConfig):
    """Config for SO devices."""

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

    def get_cavity_supported_programs(self, cavity) -> list[str]:
        """Get appliance programs."""
        cavity_capabilities = self.capabilities.get(cavity, {})
        key = self.get_property(PROGRAM)
        values = cavity_capabilities.get(key, {}).get(VALUES, {})
        return [
            program
            for program, meta in values.items()
            if not meta.get("disabled", False)
        ]

    def get_cavity_temperature_range(self, cavity, program_name: str, reported_appliance_state: dict) -> dict[
        str, float]:
        """Extract cavity temperature range for the given program based on temperature unit."""

        cavity_capabilities = self.capabilities.get(cavity, {})
        program_trigger = cavity_capabilities.get(self.get_property(PROGRAM), {}).get(VALUES, {}).get(program_name, {})
        current_unit = self.get_current_temperature_unit(reported_appliance_state)

        temperature_key = self.get_property(TARGET_TEMPERATURE_F) if current_unit == FAHRENHEIT else self.get_property(
            TARGET_TEMPERATURE_C)
        cavity_temperature_key = f"{cavity}/{self.get_property(TARGET_TEMPERATURE_F)}" if current_unit == FAHRENHEIT else f"{cavity}/{self.get_property(TARGET_TEMPERATURE_C)}"

        temp_config = program_trigger.get(cavity_temperature_key)

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

        temperature_capability = cavity_capabilities.get(temperature_key)
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

    def get_cavity_timer_range(self, cavity, program_name: str) -> dict[str, int]:
        """Extract cavity timer range for the given program."""
        cavity_capabilities = self.capabilities.get(cavity, {})

        program_trigger = cavity_capabilities.get(self.get_property(PROGRAM), {}).get(VALUES, {}).get(program_name, {})

        duration_program_config = program_trigger.get(f"{cavity}/{self.get_property(TARGET_DURATION)}")
        if duration_program_config and duration_program_config.get(DISABLED, False):
            return {
                MIN: 0,
                MAX: 0,
                STEP: 0,
            }

        if duration_program_config:
            return {
                MIN: duration_program_config.get(MIN),
                MAX: duration_program_config.get(MAX),
                STEP: duration_program_config.get(STEP),
            }

        duration_capability = cavity_capabilities.get(self.get_property(TARGET_DURATION))
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

    def get_current_temperature_unit(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current temperature unit from the reported state."""
        return self._get_state(TEMPERATURE_REPRESENTATION, reported_appliance_state)

    def get_current_alerts(self, reported_appliance_state: dict[str, Any]) -> list[Any]:
        """Get the current alerts from the reported state."""
        return self._get_state(ALERTS, reported_appliance_state)

    def get_current_remote_control(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current remote control from the reported state."""
        return self._get_state(REMOTE_CONTROL, reported_appliance_state)

    # Cavities properties
    def get_current_cavity_program(self, cavity, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current cavity program from the reported state."""
        return self._get_nested_state(cavity, self.get_property(PROGRAM), reported_appliance_state)

    def get_current_cavity_target_temperature_c(self, cavity, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current cavity target temperature C from the reported state."""
        return self._get_nested_state(cavity, self.get_property(TARGET_TEMPERATURE_C), reported_appliance_state)

    def get_current_cavity_target_temperature_f(self, cavity, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current cavity target temperature F from the reported state."""
        return self._get_nested_state(cavity, self.get_property(TARGET_TEMPERATURE_F), reported_appliance_state)

    def get_current_cavity_display_temperature_c(self, cavity, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current cavity display temperature C from the reported state."""
        return self._get_nested_state(cavity, self.get_property(DISPLAY_TEMPERATURE_C), reported_appliance_state)

    def get_current_cavity_display_temperature_f(self, cavity, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current cavity display temperature F from the reported state."""
        return self._get_nested_state(cavity, self.get_property(DISPLAY_TEMPERATURE_F), reported_appliance_state)

    def get_current_cavity_appliance_state(self, cavity, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current cavity appliance state from the reported state."""
        return self._get_nested_state(cavity, self.get_property(APPLIANCE_STATE), reported_appliance_state)

    def get_current_cavity_time_to_end(self, cavity, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current cavity time to end from the reported state."""
        return self._get_nested_state(cavity, self.get_property(TIME_TO_END), reported_appliance_state)

    def get_current_cavity_target_duration(self, cavity, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current cavity target duration from the reported state."""
        return self._get_nested_state(cavity, self.get_property(TARGET_DURATION), reported_appliance_state)

    def get_current_cavity_door_state(self, cavity, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current door state from the reported state."""
        return self._get_nested_state(cavity, self.get_property(DOOR_STATE), reported_appliance_state)

    def get_current_cavity_running_time(self, cavity, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current cavity running time from the reported state."""
        return self._get_nested_state(cavity, self.get_property(RUNNING_TIME), reported_appliance_state)

    def get_current_cavity_cavity_light(self, cavity, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current cavity cavity light from the reported state."""
        return self._get_nested_state(cavity, self.get_property(CAVITY_LIGHT), reported_appliance_state)

    def get_current_cavity_food_probe_insertion_state(self, cavity, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current cavity food probe insertion state from the reported state."""
        return self._get_nested_state(cavity, self.get_property(FOOD_PROBE_STATE), reported_appliance_state)

    def get_current_cavity_display_food_probe_temperature_f(self, cavity,
                                                            reported_appliance_state: dict[str, Any]) -> float:
        """Get the current cavity display food probe temperature f from the reported state."""
        return self._get_nested_state(cavity, self.get_property(DISPLAY_FOOD_PROBE_TEMPERATURE_F),
                                      reported_appliance_state)

    def get_current_cavity_display_food_probe_temperature_c(self, cavity,
                                                            reported_appliance_state: dict[str, Any]) -> float:
        """Get the current cavity display food probe temperature c from the reported state."""
        return self._get_nested_state(cavity, self.get_property(DISPLAY_FOOD_PROBE_TEMPERATURE_C),
                                      reported_appliance_state)

    def get_current_cavity_start_at(self, cavity, reported_appliance_state: dict[str, Any]) -> datetime:
        """Get the current cavity start at time from the reported state."""
        appliance_state = self.get_current_cavity_appliance_state(cavity, reported_appliance_state)

        if appliance_state != APPLIANCE_STATE_DELAYED_START:
            return None

        now = datetime.datetime.now(ZoneInfo("UTC"))
        start_time = self._get_nested_state(cavity, self.get_property(START_TIME),
                                            reported_appliance_state)

        if start_time is not None and start_time not in (-1, 0):
            return now + datetime.timedelta(seconds=start_time)

        return None


class SoConfigManager:
    """Manager for SO device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in SO_CONFIG."""
        self._config = SO_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> SoConfig:
        """Return the appliance_config for a given model type."""
        return SoConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
