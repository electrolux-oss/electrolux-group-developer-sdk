from typing import Any

from pydantic import PrivateAttr

from ...appliance_config.rvc_config import RvcConfig, RvcConfigManager, CLEANING_COMMAND, CLEANING_COMMAND_START, \
    CLEANING_COMMAND_RESUME, CLEANING_COMMAND_STOP, CLEANING_COMMAND_PAUSE, CLEANING_COMMAND_DOCK, MODE, CUSTOM_PLAY, \
    PERSISTENT_MAP_ID, ZONES, ZONE_ID, POWER_MODE, MAP_COMMAND, MAP_ID, ROOM_INFO, ROOM_ID, SWEEP_MODE, VACUUM_MODE, \
    WATER_PUMP_RATE, NUMBER_OF_CLEANING_REPETITIONS, CLEANING_TYPE, ROOM_NAME, ROOM_SEQUENCE
from ...client.appliances.appliance_data import ApplianceData
from ...constants import REPORTED, TYPE


class RVCAppliance(ApplianceData):
    """
    Extended appliance data class for RVC appliances.

    Adds access to capabilities and state via RvcConfig.
    """
    _config: RvcConfig = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        capabilities = self.details.capabilities if self.details else {}
        self._config = RvcConfigManager().get_config(self.appliance.applianceType, capabilities)

    def is_feature_supported(self, feature) -> bool:
        return self._config.is_capability_supported(feature)

    def get_supported_modes(self) -> list[str]:
        """Return the list of supported readable modes."""
        return self._config.get_supported_modes()

    def is_docked(self) -> bool:
        """Return true if the appliance is currently docked."""
        return self._config.is_docked(self.state.properties.get(REPORTED))

    def is_paused(self) -> bool:
        """Return true if the appliance is currently paused."""
        return self._config.is_paused(self.state.properties.get(REPORTED))

    def get_current_mode(self) -> str:
        """Return the current mode of the appliance."""
        return self._config.get_current_mode(self.state.properties.get(REPORTED))

    def get_current_state(self) -> str:
        """Return the current state of the appliance."""
        return self._config.get_current_state(self.state.properties.get(REPORTED))

    def get_battery_percentage(self) -> int:
        """Calculate and return the current battery percentage."""
        return self._config.get_battery_percentage(self.state.properties.get(REPORTED))

    def get_start_command(self) -> dict[str, Any]:
        return {
            self._config.get_property(CLEANING_COMMAND): self._config.get_property(
                CLEANING_COMMAND_START
            )
        }

    def get_resume_command(self) -> dict[str, Any]:
        return {
            self._config.get_property(CLEANING_COMMAND): self._config.get_property(
                CLEANING_COMMAND_RESUME
            )
        }

    def get_stop_command(self) -> dict[str, Any]:
        return {
            self._config.get_property(CLEANING_COMMAND): self._config.get_property(
                CLEANING_COMMAND_STOP
            )
        }

    def get_pause_command(self) -> dict[str, Any]:
        return {
            self._config.get_property(CLEANING_COMMAND): self._config.get_property(
                CLEANING_COMMAND_PAUSE
            )
        }

    def get_dock_command(self) -> dict[str, Any]:
        return {
            self._config.get_property(CLEANING_COMMAND): self._config.get_property(
                CLEANING_COMMAND_DOCK
            )
        }

    def get_set_mode_command(self, mode: str | int) -> dict[str, Any]:
        return {self._config.get_property(MODE): mode}

    def get_start_zone_cleaning_command(self, map_id: str, zone_ids: list[str], power_mode: int = 2) -> dict[str, Any]:
        if not zone_ids or not map_id:
            return {}

        return {
            CUSTOM_PLAY: {
                PERSISTENT_MAP_ID: map_id,
                ZONES: [
                    {ZONE_ID: zone_id, POWER_MODE: power_mode} for zone_id in zone_ids
                ],
            }
        }

    def get_gordias_start_room_cleaning_command(self, map_id: int,
                                                room_ids: list[int],
                                                sweep_mode: int = 0,
                                                vacuum_mode="standard",
                                                water_pump_rate="off",
                                                number_of_repetitions=1) -> dict[str, Any]:
        return {
            MAP_COMMAND: "selectRoomsClean",
            MAP_ID: map_id,
            TYPE: 1,
            ROOM_INFO: [
                {
                    ROOM_ID: room_id,
                    SWEEP_MODE: sweep_mode,
                    VACUUM_MODE: vacuum_mode,
                    WATER_PUMP_RATE: water_pump_rate,
                    NUMBER_OF_CLEANING_REPETITIONS: number_of_repetitions,
                }
                for room_id in room_ids
            ],
        }

    def get_cybele_start_room_cleaning_command(self, map_id: int,
                                               room_ids_names: list[tuple[int, str]],
                                               global_settings_cleaning: bool = True,
                                               cleaning_type="vacuum",
                                               vacuum_mode="standard",
                                               water_pump_rate="off",
                                               number_of_repetitions=1) -> dict[str, Any]:
        if global_settings_cleaning:
            return {
                MAP_COMMAND: "selectRoomsClean",
                MAP_ID: map_id,
                TYPE: 0,
                ROOM_INFO: [
                    {
                        ROOM_ID: room_id
                    }
                    for room_id, room_name in room_ids_names
                ]
            }
        else:
            return {
                MAP_COMMAND: "selectRoomsClean",
                MAP_ID: map_id,
                TYPE: 1,
                ROOM_INFO: [
                    {
                        ROOM_ID: room_id,
                        ROOM_NAME: room_name,
                        CLEANING_TYPE: cleaning_type,
                        VACUUM_MODE: vacuum_mode,
                        WATER_PUMP_RATE: water_pump_rate,
                        NUMBER_OF_CLEANING_REPETITIONS: number_of_repetitions,
                        ROOM_SEQUENCE: room_sequence
                    }
                    for room_sequence, (room_id, room_name) in enumerate(room_ids_names, start=0)
                ]
            }
