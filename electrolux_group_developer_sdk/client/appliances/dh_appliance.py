from typing import Any

from pydantic import PrivateAttr

from ...appliance_config.dh_config import DhConfig, DhConfigManager, FAN_SPEED, MODE, EXECUTE_COMMAND, \
    EXECUTE_COMMAND_ON, EXECUTE_COMMAND_OFF, TARGET_HUMIDITY, MODE_OFF
from ...client.appliances.appliance_data import ApplianceData
from ...constants import REPORTED


class DHAppliance(ApplianceData):
    """
    Extended appliance data class for DH (dehumidifier) appliances.

    Adds access to capabilities and state via DhConfig.
    """
    _config: DhConfig = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        capabilities = self.details.capabilities if self.details else {}
        self._config = DhConfigManager().get_config(self.appliance.applianceType, capabilities)

    def is_feature_supported(self, feature) -> bool:
        return self._config.is_capability_supported(feature)

    def is_appliance_on(self) -> bool:
        """Return True if the appliance is ON, False otherwise."""
        return self._config.is_appliance_on(self.state.properties.get(REPORTED))

    def get_supported_modes(self) -> list[str]:
        """Return the list of supported modes."""
        return self._config.get_supported_modes()

    def get_supported_fan_speeds(self) -> list[str]:
        """Return the list of supported fan speed settings."""
        return self._config.get_supported_fan_speeds()

    def get_supported_min_humidity(self) -> float:
        """Return the minimum humidity supported by the appliance."""
        return self._config.get_supported_min_humidity()

    def get_supported_max_humidity(self) -> float:
        """Return the maximum humidity supported by the appliance."""
        return self._config.get_supported_max_humidity()

    def get_supported_step_humidity(self) -> float:
        """Return the step increment for humidity adjustments."""
        return self._config.get_supported_step_humidity()

    def get_current_mode(self) -> str:
        """Return the current mode."""
        return self._config.get_current_mode(self.state.properties.get(REPORTED))

    def get_current_appliance_state(self) -> str:
        """Return the current appliance state of the appliance."""
        return self._config.get_current_appliance_state(self.state.properties.get(REPORTED))

    def get_current_fan_speed(self) -> str:
        """Return the current fan speed setting."""
        return self._config.get_current_fan_speed(self.state.properties.get(REPORTED))

    def get_current_target_humidity(self) -> int:
        """Return the currently target humidity."""
        return self._config.get_current_target_humidity(self.state.properties.get(REPORTED))

    def get_current_sensor_humidity(self) -> int:
        """Return the current ambient humidity."""
        return self._config.get_current_sensor_humidity(self.state.properties.get(REPORTED))

    def get_fan_speed_command(self, fan_speed) -> dict[str, Any]:
        """Return the command payload to set a new fan speed."""
        return {
            self._config.get_property(FAN_SPEED): fan_speed
        }

    def get_mode_command(self, mode) -> dict[str, Any]:
        """Return the command payload to set a new mode, or turn off if the mode is 'off'."""
        if mode == self._config.get_property(MODE_OFF):
            return self.get_turn_off_command()
        else:
            return {self._config.get_property(MODE): mode}

    def get_humidity_command(self, humidity) -> dict[str, Any]:
        """Return the command payload to set a target humidity."""
        return {
            self._config.get_property(TARGET_HUMIDITY): humidity
        }

    def get_turn_on_command(self) -> dict[str, Any]:
        """Return the command payload to turn the appliance ON."""
        return {
            self._config.get_property(EXECUTE_COMMAND): self._config.get_property(EXECUTE_COMMAND_ON)
        }

    def get_turn_off_command(self) -> dict[str, Any]:
        """Return the command payload to turn the appliance OFF."""
        return {
            self._config.get_property(EXECUTE_COMMAND): self._config.get_property(EXECUTE_COMMAND_OFF)
        }
