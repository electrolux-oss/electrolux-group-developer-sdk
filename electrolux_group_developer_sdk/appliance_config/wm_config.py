"""Washer Machine configuration."""
import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .config import ApplianceConfig
from ..constants import VALUES, WM, APPLIANCE_STATE_DELAYED_START
from ..feature_constants import *

# Configuration
WM_CONFIG = {
    WM: {
        PROGRAM_UID: "programUID",
        USER_SELECTIONS: "userSelections",
        PROGRAM_CAPABILITY: "userSelections/programUID",
        ANALOG_SPIN_SPEED: "analogSpinSpeed",
        SPIN_SPEED_CAPABILITY: "userSelections/analogSpinSpeed",
        ANALOG_TEMPERATURE: "analogTemperature",
        TEMPERATURE_CAPABILITY: "userSelections/analogTemperature",
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
        START_TIME: "startTime",
        FC_MISCELLANEOUS_STATE: "fCMiscellaneousState",
        WATER_USAGE: "waterUsage",
        WATER_USAGE_CAPABILITY: "fCMiscellaneousState/waterUsage",
        AD_TANK_B_DET_LOADED: "adTankBDetLoaded",
        AD_TANK_B_DET_LOADED_CAPABILITY: "fCMiscellaneousState/adTankBDetLoaded",
        TANK_A_DET_LOAD_FOR_NOMINAL_WEIGHT: "tankADetLoadForNominalWeight",
        TANK_A_DET_LOAD_FOR_NOMINAL_WEIGHT_CAPABILITY: "fCMiscellaneousState/tankADetLoadForNominalWeight",
        AD_TANK_B_SOFT_LOADED: "adTankBSoftLoaded",
        AD_TANK_B_SOFT_LOADED_CAPABILITY: "fCMiscellaneousState/adTankBSoftLoaded",
        ECO_LEVEL: "ecoLevel",
        ECO_LEVEL_CAPABILITY: "fCMiscellaneousState/ecoLevel",
        AD_TANK_A_DET_LOADED: "adTankADetLoaded",
        AD_TANK_A_DET_LOADED_CAPABILITY: "fCMiscellaneousState/adTankADetLoaded",
        TANK_B_DET_LOAD_FOR_NOMINAL_WEIGHT: "tankBDetLoadForNominalWeight",
        TANK_B_DET_LOAD_FOR_NOMINAL_WEIGHT_CAPABILITY: "fCMiscellaneousState/tankBDetLoadForNominalWeight",
        TANK_A_RESERVE: "tankAReserve",
        TANK_A_RESERVE_CAPABILITY: "fCMiscellaneousState/tankAReserve",
        TANK_B_RESERVE: "tankBReserve",
        TANK_B_RESERVE_CAPABILITY: "fCMiscellaneousState/tankBReserve",
    }
}


class WmConfig(ApplianceConfig):
    """Config for WM devices."""

    def get_supported_programs(self) -> list[str]:
        """Get appliance programs."""
        key = self.get_property(PROGRAM_CAPABILITY)
        values = self.capabilities.get(key, {}).get(VALUES, {})
        return [
            program
            for program, meta in values.items()
            if not meta.get("disabled", False)
        ]

    def get_supported_spin_speeds(self, program_name: str) -> list[str]:
        """Get appliance spin speeds."""

        program_trigger = self.capabilities.get(self.get_property(PROGRAM_CAPABILITY), {}).get(VALUES, {}).get(
            program_name, {})
        key = self.get_property(SPIN_SPEED_CAPABILITY)
        spin_speed_config = program_trigger.get(key)

        if spin_speed_config:
            values = spin_speed_config.get(VALUES, {})
            return [speed for speed in values if speed != "DISABLED"]

        values = self.capabilities.get(key, {}).get(VALUES, {})
        return [speed for speed in values if speed != "DISABLED"]

    def get_supported_temperature(self, program_name: str) -> list[str]:
        """Get appliance temperatures."""
        program_trigger = self.capabilities.get(self.get_property(PROGRAM_CAPABILITY), {}).get(VALUES, {}).get(
            program_name, {})
        key = self.get_property(TEMPERATURE_CAPABILITY)
        temperatures_config = program_trigger.get(key)

        if temperatures_config:
            values = temperatures_config.get(VALUES, {})
            return [temperature for temperature in values]

        values = self.capabilities.get(key, {}).get(VALUES, {})
        return [temperature for temperature in values]

    def get_current_program(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current program from the reported state."""
        return reported_appliance_state.get(self.get_property(USER_SELECTIONS)).get(self.get_property(PROGRAM_UID))

    def get_current_spin_speed(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current spin speed from the reported state."""
        return reported_appliance_state.get(self.get_property(USER_SELECTIONS)).get(
            self.get_property(ANALOG_SPIN_SPEED))

    def get_current_temperature(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current temperature from the reported state."""
        return reported_appliance_state.get(self.get_property(USER_SELECTIONS)).get(
            self.get_property(ANALOG_TEMPERATURE))

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

    def get_current_alerts(self, reported_appliance_state: dict[str, Any]) -> list[str]:
        """Get the current alerts from the reported state."""
        return self._get_state(ALERTS, reported_appliance_state)

    def get_current_f_c_miscellaneous_state_water_usage(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current water usage from the reported state."""
        return reported_appliance_state.get(self.get_property(FC_MISCELLANEOUS_STATE), {}).get(
            self.get_property(WATER_USAGE)
        )

    def get_current_f_c_miscellaneous_state_ad_tank_b_det_loaded(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current AD tank B detergent load from the reported state."""
        return reported_appliance_state.get(self.get_property(FC_MISCELLANEOUS_STATE), {}).get(
            self.get_property(AD_TANK_B_DET_LOADED)
        )

    def get_current_f_c_miscellaneous_state_tank_a_det_load_for_nominal_weight(self, reported_appliance_state: dict[
        str, Any]) -> int:
        """Get the current tank A detergent load for nominal weight from the reported state."""
        return reported_appliance_state.get(self.get_property(FC_MISCELLANEOUS_STATE), {}).get(
            self.get_property(TANK_A_DET_LOAD_FOR_NOMINAL_WEIGHT)
        )

    def get_current_f_c_miscellaneous_state_ad_tank_b_soft_loaded(self,
                                                                  reported_appliance_state: dict[str, Any]) -> int:
        """Get the current AD tank B softener load from the reported state."""
        return reported_appliance_state.get(self.get_property(FC_MISCELLANEOUS_STATE), {}).get(
            self.get_property(AD_TANK_B_SOFT_LOADED)
        )

    def get_current_f_c_miscellaneous_state_eco_level(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current eco level from the reported state."""
        return reported_appliance_state.get(self.get_property(FC_MISCELLANEOUS_STATE), {}).get(
            self.get_property(ECO_LEVEL)
        )

    def get_current_f_c_miscellaneous_state_ad_tank_a_det_loaded(self, reported_appliance_state: dict[str, Any]) -> int:
        """Get the current AD tank A detergent load from the reported state."""
        return reported_appliance_state.get(self.get_property(FC_MISCELLANEOUS_STATE), {}).get(
            self.get_property(AD_TANK_A_DET_LOADED)
        )

    def get_current_f_c_miscellaneous_state_tank_b_det_load_for_nominal_weight(self, reported_appliance_state: dict[
        str, Any]) -> int:
        """Get the current tank B detergent load for nominal weight from the reported state."""
        return reported_appliance_state.get(self.get_property(FC_MISCELLANEOUS_STATE), {}).get(
            self.get_property(TANK_B_DET_LOAD_FOR_NOMINAL_WEIGHT)
        )

    def get_current_f_c_miscellaneous_state_tank_a_reserve(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current tank A reserve status from the reported state."""
        return reported_appliance_state.get(self.get_property(FC_MISCELLANEOUS_STATE), {}).get(
            self.get_property(TANK_A_RESERVE)
        )

    def get_current_f_c_miscellaneous_state_tank_b_reserve(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Get the current tank B reserve status from the reported state."""
        return reported_appliance_state.get(self.get_property(FC_MISCELLANEOUS_STATE), {}).get(
            self.get_property(TANK_B_RESERVE)
        )

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

    def get_current_appliance_state(self, reported_appliance_state: dict[str, Any]) -> str:
        """Get the current appliance state from the reported state."""
        return self._get_state(APPLIANCE_STATE, reported_appliance_state)


class WmConfigManager:
    """Manager for WM device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in WM_CONFIG."""
        self._config = WM_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> WmConfig:
        """Return the appliance_config for a given model type."""

        return WmConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
