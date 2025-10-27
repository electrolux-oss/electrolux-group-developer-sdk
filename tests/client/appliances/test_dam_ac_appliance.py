import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.dam_ac_appliance import DAMACAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import AMBIENT_TEMPERATURE, MODE


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def dam_ac_appliance() -> DAMACAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "dam_ac_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyAC",
        applianceType="DAM_AC",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "dam_ac_state.json")

    return cast(DAMACAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(dam_ac_appliance):
    assert dam_ac_appliance.is_feature_supported(AMBIENT_TEMPERATURE) is True


def test_is_feature_supported_false(dam_ac_appliance):
    assert dam_ac_appliance.is_feature_supported("invalid_cap") is False


def test_is_ac_feature_supported_true(dam_ac_appliance):
    assert dam_ac_appliance.is_air_conditioner_feature_supported(MODE) is True


def test_is_ac_feature_supported_false(dam_ac_appliance):
    assert dam_ac_appliance.is_air_conditioner_feature_supported("invalid_cap") is False


def test_supported_modes(dam_ac_appliance):
    assert dam_ac_appliance.get_supported_modes() == ["auto", "cool", "dry", "fanOnly"]


def test_supported_fan_speeds(dam_ac_appliance):
    assert dam_ac_appliance.get_supported_fan_speeds() == ["auto", "low", "medium", "high"]


def test_get_current_mode(dam_ac_appliance):
    assert dam_ac_appliance.get_current_mode() == "cool"


def test_get_current_fan_speed(dam_ac_appliance):
    assert dam_ac_appliance.get_current_fan_speed() == "low"


def test_get_min_target_temperature(dam_ac_appliance):
    assert dam_ac_appliance.get_supported_min_temp() == 16


def test_get_max_target_temperature(dam_ac_appliance):
    assert dam_ac_appliance.get_supported_max_temp() == 32


def test_get_step_target_temperature(dam_ac_appliance):
    assert dam_ac_appliance.get_supported_step_temp() == 1


def test_get_current_unit(dam_ac_appliance):
    assert dam_ac_appliance.get_current_temperature_unit() == "CELSIUS"


def test_get_current_target_temperature(dam_ac_appliance):
    assert dam_ac_appliance.get_current_target_temperature() == 19


def test_get_current_ambient_temperature(dam_ac_appliance):
    assert dam_ac_appliance.get_current_ambient_temperature() == 25


def test_get_current_appliance_state(dam_ac_appliance):
    assert dam_ac_appliance.get_current_appliance_state() == "off"


def test_get_fan_speed_command(dam_ac_appliance):
    command = dam_ac_appliance.get_fan_speed_command("high")
    assert command == {"airConditioner": {"fanMode": "high"}}


def test_get_mode_command(dam_ac_appliance):
    command = dam_ac_appliance.get_mode_command("cool")
    assert command == {"airConditioner": {"mode": "cool"}}


def test_get_turn_on_command(dam_ac_appliance):
    command = dam_ac_appliance.get_turn_on_command()
    assert command == {"airConditioner": {"executeCommand": "on"}}


def test_get_turn_off_command(dam_ac_appliance):
    command = dam_ac_appliance.get_turn_off_command()
    assert command == {"airConditioner": {"executeCommand": "off"}}


def test_get_temperature_command(dam_ac_appliance):
    command = dam_ac_appliance.get_temperature_command(26.0)
    assert command == {"airConditioner": {"targetTemperature": 26.0}}
