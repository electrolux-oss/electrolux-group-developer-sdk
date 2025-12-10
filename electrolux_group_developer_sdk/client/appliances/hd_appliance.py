from typing import Any

from pydantic import PrivateAttr

from .appliance_data import ApplianceData
from ...appliance_config.hd_config import HdConfig, HdConfigManager, HOOD_FAN_LEVEL, LIGHT_INTENSITY, \
    LIGHT_COLOR_TEMPERATURE
from ...constants import REPORTED, MIN, STEP, MAX


class HDAppliance(ApplianceData):
    """
    Extended appliance data class for HD appliances.

    Adds access to capabilities and state via HdConfig.
    """
    _config: HdConfig = PrivateAttr()

    def __init__(self, **data: Any):
        super().__init__(**data)
        capabilities = self.details.capabilities if self.details else {}
        self._config = HdConfigManager().get_config(self.appliance.applianceType, capabilities)

    def is_feature_supported(self, feature: str | list[str]) -> bool:
        return self._config.is_capability_supported(feature)

    def get_supported_hood_fan_level(self) -> list[str]:
        """Get appliance hood fan level."""
        return self._config.get_supported_hood_fan_level()

    def get_min_light_intensity(self) -> int:
        """Get the min light intensity."""
        return self._config.get_light_intensity_range().get(MIN)

    def get_max_light_intensity(self) -> int:
        """Get the max light intensity."""
        return self._config.get_light_intensity_range().get(MAX)

    def get_step_light_intensity(self) -> int:
        """Get the step light intensity."""
        return self._config.get_light_intensity_range().get(STEP)

    def get_min_light_color_temperature_range(self) -> int:
        """Get the min light color temperature."""
        return self._config.get_light_color_temperature_range().get(MIN)

    def get_max_light_color_temperature_range(self) -> int:
        """Get the max light color temperature."""
        return self._config.get_light_color_temperature_range().get(MAX)

    def get_step_light_color_temperature_range(self) -> int:
        """Get the step light color temperature."""
        return self._config.get_light_color_temperature_range().get(STEP)

    def get_current_hood_fan_level(self) -> str:
        """Get the current hood fan level from the reported state."""
        return self._config.get_current_hood_fan_level(self.state.properties.get(REPORTED))

    def get_current_light_intensity(self) -> int:
        """Get the current light intensity from the reported state."""
        return self._config.get_current_light_intensity(self.state.properties.get(REPORTED))

    def get_current_light_color_temperature(self) -> int:
        """Get the current light color temperature from the reported state."""
        return self._config.get_current_light_color_temperature(self.state.properties.get(REPORTED))

    def get_current_hood_charc_filter_timer(self) -> int:
        """Get the current hood charc filter timer from the reported state."""
        return self._config.get_current_hood_charc_filter_timer(self.state.properties.get(REPORTED))

    def get_current_hood_filter_charc_enable(self) -> str:
        """Get the current hood filter charc enable from the reported state."""
        return self._config.get_current_hood_filter_charc_enable(self.state.properties.get(REPORTED))

    def get_current_human_centric_light_event_state(self) -> str:
        """Get the current human centric light event state from the reported state."""
        return self._config.get_current_human_centric_light_event_state(self.state.properties.get(REPORTED))

    def get_current_appliance_mode(self) -> str:
        """Get the current appliance mode from the reported state."""
        return self._config.get_current_appliance_mode(self.state.properties.get(REPORTED))

    def get_current_drawer_status(self) -> bool:
        """Get the current drawer status from the reported state."""
        return self._config.get_current_drawer_status(self.state.properties.get(REPORTED))

    def get_current_hood_grease_filter_time(self) -> int:
        """Get the current hood grease filter time from the reported state."""
        return self._config.get_current_hood_grease_filter_time(self.state.properties.get(REPORTED))

    def get_current_sound_volume(self) -> int:
        """Get the current sound volume from the reported state."""
        return self._config.get_current_sound_volume(self.state.properties.get(REPORTED))

    def get_current_tvoc_filter_time(self) -> int:
        """Get the current tvoc filter time from the reported state."""
        return self._config.get_current_tvoc_filter_time(self.state.properties.get(REPORTED))

    def get_current_hood_auto_switch_off_event(self) -> bool:
        """Get the current hood auto switch off event from the reported state."""
        return self._config.get_current_hood_auto_switch_off_event(self.state.properties.get(REPORTED))

    def get_current_appliance_state(self) -> str:
        """Get the current appliance state from the reported state."""
        return self._config.get_current_appliance_state(self.state.properties.get(REPORTED))

    def get_current_target_duration(self) -> int:
        """Get the current target duration from the reported state."""
        return self._config.get_current_target_duration(self.state.properties.get(REPORTED))

    def get_current_alerts(self) -> list[Any]:
        """Get the current alerts from the reported state."""
        return self._config.get_current_alerts(self.state.properties.get(REPORTED))

    def get_current_remote_control(self) -> str:
        """Get the current remote control from the reported state."""
        return self._config.get_current_remote_control(self.state.properties.get(REPORTED))

    def get_set_hood_fan_level_command(self, fan_level: str):
        """Return the command payload to set the hood fan level."""
        return {
            self._config.get_property(HOOD_FAN_LEVEL): fan_level}

    def get_set_light_intensity_command(self, light_intensity: int):
        """Return the command payload to set the light intensity."""
        return {
            self._config.get_property(LIGHT_INTENSITY): light_intensity}

    def get_set_light_color_temperature_command(self, light_color_temperature: int):
        """Return the command payload to set the light color temperature."""
        return {
            self._config.get_property(LIGHT_COLOR_TEMPERATURE): light_color_temperature}
