import datetime
from typing import Any

from pydantic import PrivateAttr

from .appliance_data import ApplianceData
from ...appliance_config.td_config import TdConfig, TdConfigManager, EXECUTE_COMMAND, EXECUTE_COMMAND_START, \
    EXECUTE_COMMAND_RESUME, EXECUTE_COMMAND_PAUSE, EXECUTE_COMMAND_STOP, USER_SELECTIONS, PROGRAM_UID
from ...constants import REPORTED


class TDAppliance(ApplianceData):
    """
    Extended appliance data class for TD appliances.

    Adds access to capabilities and state via TdConfig.
    """
    _config: TdConfig = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        capabilities = self.details.capabilities if self.details else {}
        self._config = TdConfigManager().get_config(self.appliance.applianceType, capabilities)

    def is_feature_supported(self, feature) -> bool:
        return self._config.is_capability_supported(feature)

    def get_supported_programs(self) -> list[str]:
        """Get appliance programs."""
        return self._config.get_supported_programs()

    def get_current_program(self) -> str:
        """Get the current program from the reported state."""
        return self._config.get_current_program(self.state.properties.get(REPORTED))

    def get_current_cycle_phase(self) -> str:
        """Get the current cycle phase from the reported state."""
        return self._config.get_current_cycle_phase(self.state.properties.get(REPORTED))

    def get_current_time_to_end(self) -> float:
        """Get the current time to end from the reported state."""
        return self._config.get_current_time_to_end(self.state.properties.get(REPORTED))

    def get_current_door_state(self) -> str:
        """Get the current door state from the reported state."""
        return self._config.get_current_door_state(self.state.properties.get(REPORTED))

    def get_current_remote_control(self) -> str:
        """Get the current remote control from the reported state."""
        return self._config.get_current_remote_control(self.state.properties.get(REPORTED))

    def get_current_water_hardness(self) -> str:
        """Get the current water hardness from the reported state."""
        return self._config.get_current_water_hardness(self.state.properties.get(REPORTED))

    def get_current_ui_lock_mode(self) -> bool:
        """Get the current ui lock mode from the reported state."""
        return self._config.get_current_ui_lock_mode(self.state.properties.get(REPORTED))

    def get_current_alerts(self) -> list[Any]:
        """Get the current alerts from the reported state."""
        return self._config.get_current_alerts(self.state.properties.get(REPORTED))

    def get_current_start_at(self) -> datetime:
        """Get the current start at time from the reported state."""
        start_at, end_at = self._config.get_current_start_at_stop_at(self.state.properties.get(REPORTED))
        return start_at

    def get_current_end_at(self) -> datetime:
        """Get the current end at time from the reported state."""
        start_at, end_at = self._config.get_current_start_at_stop_at(self.state.properties.get(REPORTED))
        return end_at

    def get_current_appliance_state(self) -> str:
        """Get the current appliance state from the reported state."""
        return self._config.get_current_appliance_state(self.state.properties.get(REPORTED))

    def get_start_command(self):
        """Return the command payload to start the appliance."""
        return {
            self._config.get_property(EXECUTE_COMMAND): self._config.get_property(EXECUTE_COMMAND_START)
        }

    def get_stop_command(self):
        """Return the command payload to stop the appliance."""
        return {
            self._config.get_property(EXECUTE_COMMAND): self._config.get_property(EXECUTE_COMMAND_STOP)
        }

    def get_resume_command(self):
        """Return the command payload to resume the appliance."""
        return {
            self._config.get_property(EXECUTE_COMMAND): self._config.get_property(EXECUTE_COMMAND_RESUME)
        }

    def get_pause_command(self):
        """Return the command payload to pause the appliance."""
        return {
            self._config.get_property(EXECUTE_COMMAND): self._config.get_property(EXECUTE_COMMAND_PAUSE)
        }

    def get_set_program_command(self, program: str):
        """Return the command payload to set the program."""
        return {
            self._config.get_property(USER_SELECTIONS): {
                self._config.get_property(PROGRAM_UID): program}
        }
