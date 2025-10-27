import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.hd_appliance import HDAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import LIGHT_INTENSITY


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def hd_appliance() -> HDAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "hd_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyHD",
        applianceType="HD",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "hd_state.json")

    return cast(HDAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(hd_appliance):
    assert hd_appliance.is_feature_supported(LIGHT_INTENSITY) is True


def test_is_feature_supported_false(hd_appliance):
    assert hd_appliance.is_feature_supported("invalid_cap") is False


def test_get_supported_hood_fan_level(hd_appliance):
    assert sorted(hd_appliance.get_supported_hood_fan_level()) == ['BOOST', 'BOOST_2', 'BREEZE', 'OFF', 'STEP_1',
                                                                   'STEP_2', 'STEP_3']


def test_get_min_light_intensity(hd_appliance):
    assert hd_appliance.get_min_light_intensity() == 0


def test_get_max_light_intensity(hd_appliance):
    assert hd_appliance.get_max_light_intensity() == 100


def test_get_step_light_intensity(hd_appliance):
    assert hd_appliance.get_step_light_intensity() == 1


def test_get_min_light_color_temperature_range(hd_appliance):
    assert hd_appliance.get_min_light_color_temperature_range() == 0


def test_get_max_light_color_temperature_range(hd_appliance):
    assert hd_appliance.get_max_light_color_temperature_range() == 100


def test_get_step_light_color_temperature_range(hd_appliance):
    assert hd_appliance.get_step_light_color_temperature_range() == 1


def test_get_current_hood_fan_level(hd_appliance):
    assert hd_appliance.get_current_hood_fan_level() == "OFF"


def test_get_current_light_intensity(hd_appliance):
    assert hd_appliance.get_current_light_intensity() == 0


def test_get_current_light_color_temperature(hd_appliance):
    assert hd_appliance.get_current_light_color_temperature() == 0


def test_get_current_hood_charc_filter_timer(hd_appliance):
    assert hd_appliance.get_current_hood_charc_filter_timer() == 0


def test_get_current_hood_filter_charc_enable(hd_appliance):
    assert hd_appliance.get_current_hood_filter_charc_enable() == "OFF"


def test_get_current_human_centric_light_event_state(hd_appliance):
    assert hd_appliance.get_current_human_centric_light_event_state() == "OFF"


def test_get_current_appliance_mode(hd_appliance):
    assert hd_appliance.get_current_appliance_mode() == "NORMAL"


def test_get_current_drawer_status(hd_appliance):
    assert hd_appliance.get_current_drawer_status() == False


def test_get_current_hood_grease_filter_time(hd_appliance):
    assert hd_appliance.get_current_hood_grease_filter_time() == 0


def test_get_current_sound_volume(hd_appliance):
    assert hd_appliance.get_current_sound_volume() == 0


def test_get_current_tvoc_filter_time(hd_appliance):
    assert hd_appliance.get_current_tvoc_filter_time() == 918000


def test_get_current_hood_auto_switch_off_event(hd_appliance):
    assert hd_appliance.get_current_hood_auto_switch_off_event() == False


def test_get_current_appliance_state(hd_appliance):
    assert hd_appliance.get_current_appliance_state() == "OFF"


def test_get_current_target_duration(hd_appliance):
    assert hd_appliance.get_current_target_duration() == 0


def test_get_current_alerts(hd_appliance):
    assert hd_appliance.get_current_alerts() == []


def test_get_current_remote_control(hd_appliance):
    assert hd_appliance.get_current_remote_control() == "ENABLED"


def test_get_set_hood_fan_level_command(hd_appliance):
    cmd = hd_appliance.get_set_hood_fan_level_command("STEP_1")
    assert cmd == {"hoodFanLevel": "STEP_1"}


def test_get_set_light_intensity_command(hd_appliance):
    cmd = hd_appliance.get_set_light_intensity_command(20)
    assert cmd == {"lightIntensity": 20}


def test_get_set_light_color_temperature_command(hd_appliance):
    cmd = hd_appliance.get_set_light_color_temperature_command(30)
    assert cmd == {"lightColorTemperature": 30}
