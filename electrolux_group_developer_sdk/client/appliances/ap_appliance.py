from typing import Any

from pydantic import PrivateAttr

from .appliance_data import ApplianceData
from ...appliance_config.ap_config import ApConfig, ApConfigManager, FAN_SPEED, WORKMODE, POWER_COMMAND, \
    POWER_OFF_COMMAND, POWER_ON_COMMAND, WORKMODE_POWER_OFF
from ...constants import REPORTED


class APAppliance(ApplianceData):
    """
    Extended appliance data class for AP appliances.

    Adds access to capabilities and state via ApConfig.
    """
    _config: ApConfig = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        capabilities = self.details.capabilities if self.details else {}
        self._config = ApConfigManager().get_config(self.appliance.applianceType, capabilities)

    def is_feature_supported(self, feature) -> bool:
        return self._config.is_capability_supported(feature)

    def get_air_quality_map(self) -> dict[str, str]:
        """Return the air quality map."""
        return self._config.get_air_quality_map()

    def get_supported_modes(self) -> list[str]:
        """Return a list of supported modes."""
        return self._config.get_supported_modes()

    def get_supported_min_fan_speed(self) -> int:
        """Return the minimum supported fan speed."""
        return self._config.get_min_fan_speed()

    def get_supported_max_fan_speed(self) -> int:
        """Return the maximum supported fan speed."""
        return self._config.get_max_fan_speed()

    def get_off_mode(self) -> str:
        """Return the mode representing 'OFF' state."""
        return self._config.get_property(WORKMODE_POWER_OFF)

    def get_current_mode(self) -> str:
        """Return the current mode of the appliance."""
        return self._config.get_current_mode(self.state.properties.get(REPORTED))

    def is_appliance_on(self) -> bool:
        """Return True if the appliance is currently ON, False otherwise."""
        return self._config.is_appliance_on(self.state.properties.get(REPORTED))

    def get_current_fan_speed(self) -> int:
        """Return the current fan speed setting."""
        return self._config.get_current_fan_speed(self.state.properties.get(REPORTED))

    def get_current_air_quality(self, air_quality_property: str) -> float:
        """Return the current air quality value for the specified property."""
        return self._config.get_air_quality(self.state.properties.get(REPORTED), air_quality_property)

    def get_fan_speed_command(self, fan_speed) -> dict[str, int]:
        """Return the command payload to set the fan speed."""
        return {
            self._config.get_property(FAN_SPEED): fan_speed
        }

    def get_mode_command(self, mode) -> dict[str, str]:
        """Return the command payload to set the mode."""
        return {
            self._config.get_property(WORKMODE): mode
        }

    def get_turn_on_command(self) -> dict[str, Any]:
        """Return the command payload to turn the appliance ON."""
        return {
            self._config.get_property(POWER_COMMAND): self._config.get_property(POWER_ON_COMMAND)
        }

    def get_turn_off_command(self) -> dict[str, Any]:
        """Return the command payload to turn the appliance OFF."""
        return {
            self._config.get_property(POWER_COMMAND): self._config.get_property(POWER_OFF_COMMAND)
        }
