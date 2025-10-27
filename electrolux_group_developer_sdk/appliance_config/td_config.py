"""Tumble Dryer configuration."""
import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .config import ApplianceConfig
from ..constants import VALUES, TD, APPLIANCE_STATE_DELAYED_START
from ..feature_constants import *

# Configuration
TD_CONFIG = {
    TD: {
        PROGRAM_UID: "programUID",
        USER_SELECTIONS: "userSelections",
        PROGRAM_CAPABILITY: "userSelections/programUID",
        EXECUTE_COMMAND: "executeCommand",
        APPLIANCE_STATE: "applianceState",
        CYCLE_PHASE: "cyclePhase",
        TIME_TO_END: "timeToEnd",
        EXECUTE_COMMAND_START: "START",
        EXECUTE_COMMAND_STOP: "STOPRESET",
        EXECUTE_COMMAND_PAUSE: "PAUSE",
        EXECUTE_COMMAND_RESUME: "RESUME",
        REMOTE_CONTROL: "remoteControl",
        DOOR_STATE: "doorState",
        UI_LOCK_MODE: "uiLockMode",
        WATER_HARDNESS: "waterHardness",
        ALERTS: "alerts",
        STOP_TIME: "stopTime",
        START_TIME: "startTime"
    }
}


class TdConfig(ApplianceConfig):
    """Config for TD devices."""

    def get_supported_programs(self) -> list[str]:
        """Get appliance programs."""
        key = self.get_property(PROGRAM_CAPABILITY)
        values = self.capabilities.get(key, {}).get(VALUES, {})
        return [
            program
            for program, meta in values.items()
            if not meta.get("disabled", False)
        ]

    def get_current_program(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current program from the reported state."""
        return reported_appliance_state.get(self.get_property(USER_SELECTIONS)).get(self.get_property(PROGRAM_UID))

    def get_current_cycle_phase(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current cycle phase from the reported state."""
        return self._get_state(CYCLE_PHASE, reported_appliance_state)

    def get_current_time_to_end(self, reported_appliance_state: dict[str, Any]) -> float:
        """Get the current time to end from the reported state."""
        return self._get_state(TIME_TO_END, reported_appliance_state)

    def get_current_door_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current door state from the reported state."""
        return self._get_state(DOOR_STATE, reported_appliance_state)

    def get_current_remote_control(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current remote control from the reported state."""
        return self._get_state(REMOTE_CONTROL, reported_appliance_state)

    def get_current_water_hardness(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current water hardness from the reported state."""
        return self._get_state(WATER_HARDNESS, reported_appliance_state)

    def get_current_ui_lock_mode(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current ui lock mode from the reported state."""
        return self._get_state(UI_LOCK_MODE, reported_appliance_state)

    def get_current_alerts(self, reported_appliance_state: dict[str, Any]) -> list[Any]:
        """Get the current alerts from the reported state."""
        return self._get_state(ALERTS, reported_appliance_state)

    def get_current_appliance_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current appliance state from the reported state."""
        return self._get_state(APPLIANCE_STATE, reported_appliance_state)

    def get_current_start_at_stop_at(self, reported_appliance_state: dict[str, Any]) -> tuple[datetime, datetime]:
        """Get the current start at time and end at time from the reported state."""
        appliance_state = self.get_current_appliance_state(reported_appliance_state)

        if appliance_state != APPLIANCE_STATE_DELAYED_START:
            return None, None

        stop_time = self._get_state(STOP_TIME, reported_appliance_state)
        time_to_end = self.get_current_time_to_end(reported_appliance_state)
        now = datetime.datetime.now(ZoneInfo("UTC"))

        if stop_time is not None and stop_time not in (-1, 0):
            end_at = now + datetime.timedelta(seconds=stop_time)
            start_at = end_at - datetime.timedelta(seconds=time_to_end)
            return start_at, end_at

        start_time = self._get_state(START_TIME, reported_appliance_state)

        if start_time is not None and start_time not in (-1, 0):
            start_at = now + datetime.timedelta(seconds=start_time)
            end_at = start_at + datetime.timedelta(seconds=time_to_end)

            return start_at, end_at
        return None, None


class TdConfigManager:
    """Manager for TD device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in TD_CONFIG."""
        self._config = TD_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> TdConfig:
        """Return the appliance_config for a given model type."""

        return TdConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
