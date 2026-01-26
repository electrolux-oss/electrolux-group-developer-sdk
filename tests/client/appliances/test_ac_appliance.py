import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.ac_appliance import ACAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import FAN_SPEED_SETTING


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def ac_appliance() -> ACAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "ac_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyAC",
        applianceType="AC",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "ac_state.json")

    return cast(ACAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(ac_appliance):
    assert ac_appliance.is_feature_supported(FAN_SPEED_SETTING) is True


def test_is_feature_supported_false(ac_appliance):
    assert ac_appliance.is_feature_supported("invalid_cap") is False


def test_supported_modes(ac_appliance):
    assert ac_appliance.get_supported_modes() == ["COOL", "ECO", "FANONLY", "OFF"]


def test_supported_fan_speeds(ac_appliance):
    assert ac_appliance.get_supported_fan_speeds() == ["AUTO", "HIGH", "LOW", "MIDDLE"]


def test_get_current_mode(ac_appliance):
    assert ac_appliance.get_current_mode() == "OFF"


def test_get_current_fan_speed(ac_appliance):
    assert ac_appliance.get_current_fan_speed() == "LOW"


def test_get_min_target_temperature(ac_appliance):
    assert ac_appliance.get_supported_min_temp() == 15.56


def test_get_max_target_temperature(ac_appliance):
    assert ac_appliance.get_supported_max_temp() == 32.22


def test_get_step_target_temperature(ac_appliance):
    assert ac_appliance.get_supported_step_temp() == 1.0


def test_get_current_unit_from_state(ac_appliance):
    assert ac_appliance.get_current_temperature_unit() == "CELSIUS"


def test_get_current_unit_from_state_fahrenheit(ac_appliance):
    ac_appliance.state.properties["reported"]["temperatureRepresentation"] = "FAHRENHEIT"

    assert ac_appliance.get_current_temperature_unit() == "FAHRENHEIT"


def test_get_current_unit_from_capabilities(ac_appliance):
    ac_appliance.state.properties["reported"].pop("temperatureRepresentation")

    assert ac_appliance.get_current_temperature_unit() == "CELSIUS"


def test_get_current_unit_from_capabilities_default(ac_appliance):
    ac_appliance.state.properties["reported"].pop("temperatureRepresentation")
    ac_appliance._config.capabilities.pop("targetTemperatureC", "")
    ac_appliance._config.capabilities.pop("targetTemperatureF", "")

    assert ac_appliance.get_current_temperature_unit() == "CELSIUS"


def test_get_current_unit_from_capabilities_fahrenheit(ac_appliance):
    ac_appliance.state.properties["reported"].pop("temperatureRepresentation")
    ac_appliance._config.capabilities.pop("targetTemperatureC", "")

    assert ac_appliance.get_current_temperature_unit() == "FAHRENHEIT"


def test_get_current_target_temperature_c(ac_appliance):
    assert ac_appliance.get_current_target_temperature_c() == 26.0


def test_get_current_target_temperature_f(ac_appliance):
    assert ac_appliance.get_current_target_temperature_f() == 78.8


def test_get_current_ambient_temperature_f(ac_appliance):
    assert ac_appliance.get_current_ambient_temperature_f() == 71.6


def test_get_current_ambient_temperature_c(ac_appliance):
    assert ac_appliance.get_current_ambient_temperature_c() == 22.0


def test_get_current_appliance_state(ac_appliance):
    assert ac_appliance.get_current_appliance_state() == "OFF"


def test_get_fan_speed_command(ac_appliance):
    command = ac_appliance.get_fan_speed_command("MIDDLE")
    assert isinstance(command, dict)
    assert "fanSpeedSetting" in command
    assert command["fanSpeedSetting"] == "MIDDLE"


def test_get_mode_command(ac_appliance):
    command = ac_appliance.get_mode_command("COOL")
    assert command == {"mode": "COOL"}


def test_get_turn_on_command(ac_appliance):
    command = ac_appliance.get_turn_on_command()
    assert command == {"executeCommand": "ON"}


def test_get_turn_off_command(ac_appliance):
    command = ac_appliance.get_turn_off_command()
    assert command == {"executeCommand": "OFF"}


def test_get_temperature_c_command(ac_appliance):
    command = ac_appliance.get_temperature_c_command(26.0)
    assert command == {"targetTemperatureC": 26.0}


def test_get_temperature_f_command(ac_appliance):
    command = ac_appliance.get_temperature_f_command(70.0)
    assert command == {"targetTemperatureF": 70.0}
