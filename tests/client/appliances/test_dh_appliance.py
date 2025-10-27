import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.dh_appliance import DHAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import MODE


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def dh_appliance() -> DHAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "dh_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyDH",
        applianceType="DH",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "dh_state.json")

    return cast(DHAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(dh_appliance):
    assert dh_appliance.is_feature_supported(MODE) is True


def test_is_feature_supported_false(dh_appliance):
    assert dh_appliance.is_feature_supported("invalid_cap") is False


def test_is_appliance_on(dh_appliance):
    assert dh_appliance.is_appliance_on() is False


def test_get_supported_modes(dh_appliance):
    assert sorted(dh_appliance.get_supported_modes()) == ["AUTO", "CONTINUOUS", "DRY", "OFF", "QUIET"]


def test_get_supported_fan_speeds(dh_appliance):
    assert sorted(dh_appliance.get_supported_fan_speeds()) == ["HIGH", "LOW", "MIDDLE"]


def test_get_supported_min_humidity(dh_appliance):
    assert dh_appliance.get_supported_min_humidity() == 35


def test_get_supported_max_humidity(dh_appliance):
    assert dh_appliance.get_supported_max_humidity() == 85


def test_get_supported_step_humidity(dh_appliance):
    assert dh_appliance.get_supported_step_humidity() == 5


def test_get_current_mode(dh_appliance):
    assert dh_appliance.get_current_mode() == "OFF"


def test_get_current_appliance_state(dh_appliance):
    assert dh_appliance.get_current_appliance_state() == "OFF"


def test_get_current_fan_speed(dh_appliance):
    assert dh_appliance.get_current_fan_speed() == "HIGH"


def test_get_current_target_humidity(dh_appliance):
    assert dh_appliance.get_current_target_humidity() == 35


def test_get_current_sensor_humidity(dh_appliance):
    assert dh_appliance.get_current_sensor_humidity() == 50


def test_get_fan_speed_command(dh_appliance):
    cmd = dh_appliance.get_fan_speed_command("LOW")
    assert cmd == {"fanSpeedSetting": "LOW"}


def test_get_mode_command_normal(dh_appliance):
    cmd = dh_appliance.get_mode_command("DRY")
    assert cmd == {"mode": "DRY"}


def test_get_humidity_command(dh_appliance):
    cmd = dh_appliance.get_humidity_command(50)
    assert cmd == {"targetHumidity": 50}


def test_get_turn_on_command(dh_appliance):
    cmd = dh_appliance.get_turn_on_command()
    assert cmd == {"executeCommand": "ON"}


def test_get_turn_off_command(dh_appliance):
    cmd = dh_appliance.get_turn_off_command()
    assert cmd == {"executeCommand": "OFF"}
