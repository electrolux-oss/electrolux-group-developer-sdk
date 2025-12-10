"""RVC configuration."""
from typing import Any

from pydantic import computed_field

from .config import ApplianceConfig
from ..constants import GORDIAS, PUREI9, SERIES_700, VALUES, MIN, MAX, TYPE, TYPE_STRING, TYPE_INT, CYBELE
from ..feature_constants import *

# Constant
CUSTOM_PLAY = "CustomPlay"
PERSISTENT_MAP_ID = "persistentMapId"
ZONES = "zones"
ZONE_ID = "zoneId"
POWER_MODE = "powerMode"
MAP_COMMAND = "mapCommand"
MAP_ID = "mapId"
ROOM_INFO = "roomInfo"
ROOM_ID = "roomId"
ROOM_NAME = "roomName"
ROOM_SEQUENCE = "roomSequence"
CLEANING_TYPE = "cleaningType"
SWEEP_MODE = "sweepMode"
VACUUM_MODE = "vacuumMode"
WATER_PUMP_RATE = "waterPumpRate"
NUMBER_OF_CLEANING_REPETITIONS = "numberOfCleaningRepetitions"

# Configuration
RVC_CONFIG = {
    PUREI9: {
        STATE: "robotStatus",
        DOCKED: "robotStatus",
        IS_DOCKED_MAP: {
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: True,
            10: False,
            11: False,
            12: True,
            13: False,
            14: False,
        },
        IS_PAUSED_MAP: {
            1: False,
            2: True,
            3: False,
            4: True,
            5: False,
            6: True,
            7: False,
            8: True,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
        },
        CLEANING_COMMAND: "CleaningCommand",
        CLEANING_COMMAND_START: "play",
        CLEANING_COMMAND_STOP: "stop",
        CLEANING_COMMAND_PAUSE: "pause",
        CLEANING_COMMAND_RESUME: "play",
        CLEANING_COMMAND_DOCK: "home",
        BATTERY: "batteryStatus",
        MODE: "powerMode"
    },
    GORDIAS: {
        STATE: "state",
        DOCKED: "chargingStatus",
        IS_DOCKED_MAP: {"idle": False, "charging": True, "fullyCharged": True},
        IS_PAUSED_MAP: {
            "inProgress": False,
            "goingHome": False,
            "idle": False,
            "paused": True,
            "sleeping": False
        },
        CLEANING_COMMAND: "cleaningCommand",
        CLEANING_COMMAND_START: "startGlobalClean",
        CLEANING_COMMAND_STOP: "stopClean",
        CLEANING_COMMAND_PAUSE: "pauseClean",
        CLEANING_COMMAND_RESUME: "resumeClean",
        CLEANING_COMMAND_DOCK: "startGoToCharger",
        BATTERY: "batteryStatus",
        MODE: "vacuumMode"
    },
    CYBELE: {
        STATE: "state",
        DOCKED: "chargingStatus",
        IS_DOCKED_MAP: {"idle": False, "charging": True, "fullyCharged": True},
        IS_PAUSED_MAP: {
            "inProgress": False,
            "goingHome": False,
            "idle": False,
            "paused": True,
            "sleeping": False,
            "vacuuming": False,
            "mopping": False,
            "vaccumAndMopping": False,
            "pitStop": False,
            "stationAction": False
        },
        CLEANING_COMMAND: "cleaningCommand",
        CLEANING_COMMAND_START: "startGlobalClean",
        CLEANING_COMMAND_STOP: "stopClean",
        CLEANING_COMMAND_PAUSE: "pauseClean",
        CLEANING_COMMAND_RESUME: "resumeClean",
        CLEANING_COMMAND_DOCK: "startGoToCharger",
        BATTERY: "batteryStatus",
        MODE: "vacuumMode"
    },
    SERIES_700: {
        STATE: "state",
        DOCKED: "chargingStatus",
        IS_DOCKED_MAP: {"idle": False, "charging": True, "fullyCharged": True},
        IS_PAUSED_MAP: {
            "inProgress": False,
            "goingHome": False,
            "idle": False,
            "paused": True,
            "sleeping": False
        },
        CLEANING_COMMAND: "cleaningCommand",
        CLEANING_COMMAND_START: "startGlobalClean",
        CLEANING_COMMAND_STOP: "stopClean",
        CLEANING_COMMAND_PAUSE: "pauseClean",
        CLEANING_COMMAND_RESUME: "resumeClean",
        CLEANING_COMMAND_DOCK: "startGoToCharger",
        BATTERY: "batteryStatus",
        MODE: "vacuumMode"
    },
}


class RvcConfig(ApplianceConfig):
    """Config for RVC devices."""

    @computed_field
    @property
    def _is_docked_map(self) -> dict[str, Any]:
        return self.mapping.get(IS_DOCKED_MAP, {})

    @computed_field
    @property
    def _is_paused_map(self) -> dict[str, Any]:
        return self.mapping.get(IS_PAUSED_MAP, {})

    def get_supported_modes(self) -> list[int] | list[str]:
        """Return the list of supported readable modes."""
        mode_capability = self.capabilities.get(self.get_property(MODE))
        if not mode_capability:
            return []
        # Purei
        if mode_capability.get(TYPE) == TYPE_INT:
            min_val = mode_capability.get(MIN, 0)
            max_val = mode_capability.get(MAX, 0)
            return [mode for mode in range(min_val, max_val + 1)]

        # 700 series, Gordias, Cybele
        if mode_capability.get(TYPE) == TYPE_STRING:
            values = mode_capability.get(VALUES, {})
            return [mode for mode in values]

        return []

    def is_docked(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Return true if the appliance is currently docked."""
        reported_value = self._get_state(DOCKED, reported_appliance_state)
        return self._is_docked_map[reported_value] or False

    def is_paused(self, reported_appliance_state: dict[str, Any]) -> bool:
        """Return true if the appliance is currently paused."""
        reported_value = self._get_state(STATE, reported_appliance_state)
        return self._is_paused_map[reported_value] or False

    def get_current_mode(self, reported_appliance_state: dict[str, Any]) -> str | int:
        """Return the current mode of the appliance."""
        return self._get_state(MODE, reported_appliance_state)

    def get_current_state(self, reported_appliance_state: dict[str, Any]) -> str | int:
        """Return the current state of the appliance."""
        return self._get_state(STATE, reported_appliance_state)

    def get_battery_percentage(self, reported_appliance_state: dict[str, Any]) -> int | int:
        """Calculate and return the current battery percentage."""
        capability = self.capabilities.get(self.get_property(BATTERY))

        if not capability:
            return 0

        reported_value = self._get_state(BATTERY, reported_appliance_state)

        if not reported_value:
            return 0

        max_val = capability.get(MAX, 100)
        return round((reported_value / max_val) * 100)


class RvcConfigManager:
    """Manager for RVC device configuration by model."""

    def __init__(self) -> None:
        """Initialize with configuration data in RVC_CONFIG."""
        self._config = RVC_CONFIG

    def get_config(self, model_type: str, capabilities: dict[str, Any]) -> RvcConfig:
        """Return the appliance_config for a given model type."""

        return RvcConfig(mapping=self._config.get(model_type, {}), capabilities=capabilities)
