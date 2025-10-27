import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from electrolux_group_developer_sdk.appliance_config.ap_config import PM_2_5
from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.ap_appliance import APAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import FAN_SPEED


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def ap_appliance() -> APAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "ap_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyAP",
        applianceType="Muju",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "ap_state.json")

    return cast(APAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(ap_appliance):
    assert ap_appliance.is_feature_supported(FAN_SPEED) is True


def test_is_feature_supported_false(ap_appliance):
    assert ap_appliance.is_feature_supported("invalid_cap") is False


def test_get_air_quality_map(ap_appliance):
    air_quality_map = ap_appliance.get_air_quality_map()
    assert "PM_2_5" in air_quality_map.keys()
    assert "PM_10" in air_quality_map.keys()


def test_get_supported_modes(ap_appliance):
    assert ap_appliance.get_supported_modes() == ["Manual", "PowerOff", "Quiet", "Smart"]


def test_get_supported_fan_speed_range(ap_appliance):
    assert ap_appliance.get_supported_min_fan_speed() == 1
    assert ap_appliance.get_supported_max_fan_speed() == 3


def test_get_off_mode(ap_appliance):
    assert ap_appliance.get_off_mode() == "PowerOff"


def test_get_current_mode(ap_appliance):
    assert ap_appliance.get_current_mode() == "Auto"


def test_is_appliance_on(ap_appliance):
    assert ap_appliance.is_appliance_on() is True


def test_get_current_fan_speed(ap_appliance):
    assert ap_appliance.get_current_fan_speed() == 1


def test_get_current_air_quality(ap_appliance):
    assert ap_appliance.get_current_air_quality(PM_2_5) == 4.5


def test_get_fan_speed_command(ap_appliance):
    cmd = ap_appliance.get_fan_speed_command(4)
    assert cmd == {"Fanspeed": 4}


def test_get_mode_command(ap_appliance):
    cmd = ap_appliance.get_mode_command("Quiet")
    assert cmd == {"Workmode": "Quiet"}


def test_get_turn_on_command(ap_appliance):
    cmd = ap_appliance.get_turn_on_command()
    assert cmd == {"Workmode": "Manual"}


def test_get_turn_off_command(ap_appliance):
    cmd = ap_appliance.get_turn_off_command()
    assert cmd == {"Workmode": "PowerOff"}
