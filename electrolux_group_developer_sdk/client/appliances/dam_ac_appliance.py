from typing import Any

from pydantic import PrivateAttr

from .appliance_data import ApplianceData
from ...appliance_config.dam_ac_config import DamAcConfig, DamAcConfigManager
from ...appliance_config.dam_ac_config import FAN_MODE, MODE, TARGET_TEMPERATURE, \
    EXECUTE_COMMAND, AIR_CONDITIONER
from ...constants import REPORTED


class DAMACAppliance(ApplianceData):
    """
    Extended appliance data class for DAM AC appliances.

    Adds access to capabilities and state via DamAcConfig.
    """
    _config: DamAcConfig = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        capabilities = self.details.capabilities if self.details else {}
        self._config = DamAcConfigManager().get_config(self.appliance.applianceType, capabilities)

    def is_feature_supported(self, feature: str | list[str]) -> bool:
        return self._config.is_capability_supported(feature)

    def is_air_conditioner_feature_supported(self, feature: str) -> bool:
        return self._config.is_air_conditioner_capability_supported(feature)

    def get_supported_modes(self) -> list[str]:
        """Return a list of supported modes."""
        return self._config.get_supported_modes()

    def get_supported_fan_speeds(self) -> list[str]:
        """Return a list of supported fan speeds."""
        return self._config.get_supported_fan_speeds()

    def get_supported_min_temp(self) -> float:
        """Return the minimum supported temperature."""
        return self._config.get_supported_min_temp()

    def get_supported_max_temp(self) -> float:
        """Return the maximum supported temperature."""
        return self._config.get_supported_max_temp()

    def get_supported_step_temp(self) -> float:
        """Return the step increment for temperature control."""
        return self._config.get_supported_step_temp()

    def get_current_mode(self) -> str:
        """Return the current mode."""
        return self._config.get_current_mode(self.state.properties.get(REPORTED))

    def get_current_temperature_unit(self) -> str:
        """Return the current temperature unit. Temperature unit is always Celsius for DAM AC."""
        return self._config.get_current_temperature_unit()

    def get_current_target_temperature(self) -> float:
        """Return the current target temperature in Celsius."""
        return self._config.get_current_target_temperature(self.state.properties.get(REPORTED))

    def get_current_ambient_temperature(self) -> float:
        """Return the current ambient temperature in Celsius."""
        return self._config.get_current_ambient_temperature(self.state.properties.get(REPORTED))

    def get_current_appliance_state(self) -> str:
        """Return the current appliance state."""
        return self._config.get_current_appliance_state(self.state.properties.get(REPORTED))

    def get_current_fan_speed(self) -> str:
        """Return the current fan speed setting."""
        return self._config.get_current_fan_speed(self.state.properties.get(REPORTED))

    def get_fan_speed_command(self, fan_speed: str) -> dict[str, Any]:
        """Return the command payload to set the fan speed."""
        return {
            self._config.get_property(AIR_CONDITIONER): {
                self._config.get_property(FAN_MODE): fan_speed
            }
        }

    def get_mode_command(self, mode: str) -> dict[str, Any]:
        """Return the command payload to set the mode."""
        return {
            self._config.get_property(AIR_CONDITIONER): {
                self._config.get_property(MODE): mode
            }
        }

    def get_temperature_command(self, temperature: float) -> dict[str, Any]:
        """Return the command payload to set the temperature in Celsius."""
        return {
            self._config.get_property(AIR_CONDITIONER): {
                self._config.get_property(TARGET_TEMPERATURE): temperature
            }
        }

    def get_turn_on_command(self) -> dict[str, Any]:
        """Return the command payload to turn the appliance ON."""
        return {
            self._config.get_property(AIR_CONDITIONER): {
                self._config.get_property(EXECUTE_COMMAND): "on"
            }
        }

    def get_turn_off_command(self) -> dict[str, Any]:
        """Return the command payload to turn the appliance OFF."""
        return {
            self._config.get_property(AIR_CONDITIONER): {
                self._config.get_property(EXECUTE_COMMAND): "off"
            }
        }
