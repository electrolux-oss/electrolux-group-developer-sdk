import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.hb_appliance import HBAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import CHILD_LOCK, HOOD_STATE, ZONE_RESIDUAL_HEAT_STATE


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def hb_appliance() -> HBAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "hb_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyHB",
        applianceType="HB",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "hb_state.json")

    return cast(HBAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(hb_appliance):
    assert hb_appliance.is_feature_supported(CHILD_LOCK) is True


def test_is_feature_supported_false(hb_appliance):
    assert hb_appliance.is_feature_supported("invalid_cap") is False


def test_is_hood_feature_supported_true(hb_appliance):
    assert hb_appliance.is_hood_feature_supported(HOOD_STATE) is True


def test_is_hood_feature_supported_false(hb_appliance):
    assert hb_appliance.is_hood_feature_supported("invalid_cap") is False


def test_is_hob_zone_feature_supported_true(hb_appliance):
    assert hb_appliance.is_hob_zone_feature_supported("hobZone1", ZONE_RESIDUAL_HEAT_STATE) is True


def test_is_hob_zone_feature_supported_false(hb_appliance):
    assert hb_appliance.is_hob_zone_feature_supported("hobZone1", "invalid_cap") is False


def test_get_supported_hood_fan_speed(hb_appliance):
    assert sorted(hb_appliance.get_supported_hood_fan_speed()) == ['BOOST', 'BREEZE', 'OFF', 'STEP_1', 'STEP_2',
                                                                   'STEP_3']


def test_get_supported_hood_state(hb_appliance):
    assert sorted(hb_appliance.get_supported_hood_state()) == ['AUTOMATIC', 'MANUAL']


def test_get_supported_key_sound_tone(hb_appliance):
    assert sorted(hb_appliance.get_supported_key_sound_tone()) == ['CLICK', 'NONE']


def test_get_available_hob_zone(hb_appliance):
    assert sorted(hb_appliance.get_available_hob_zone()) == ['hobZone1', 'hobZone2', 'hobZone3', 'hobZone4']


def test_get_current_hood_fan_speed(hb_appliance):
    assert hb_appliance.get_current_hood_fan_speed() == "OFF"


def test_get_current_hood_state(hb_appliance):
    assert hb_appliance.get_current_hood_state() == "AUTO_SUSPEND"


def test_get_current_key_sound_tone(hb_appliance):
    assert hb_appliance.get_current_key_sound_tone() == "NONE"


def test_get_current_child_lock(hb_appliance):
    assert hb_appliance.get_current_child_lock() == False


def test_get_current_appliance_state(hb_appliance):
    assert hb_appliance.get_current_appliance_state() == "OFF"


def test_get_current_alerts(hb_appliance):
    assert hb_appliance.get_current_alerts() == []


def test_get_current_remote_control(hb_appliance):
    assert hb_appliance.get_current_remote_control() == "NOT_SAFETY_RELEVANT_ENABLED"


def test_get_current_ui_lock_mode(hb_appliance):
    assert hb_appliance.get_current_ui_lock_mode() == False


def test_get_current_appliance_mode(hb_appliance):
    assert hb_appliance.get_current_appliance_mode() == "NORMAL"


def test_get_current_hob_hood_window_notification(hb_appliance):
    assert hb_appliance.get_current_hob_hood_window_notification() == "NONE"


def test_get_current_hob_hood_target_duration(hb_appliance):
    assert hb_appliance.get_current_hob_hood_target_duration() == 0


@pytest.mark.parametrize(
    "zone_key,expected_value",
    [
        ("hobZone1", "NO"),
        ("hobZone2", "NO"),
        ("hobZone3", "NO"),
        ("hobZone4", "NO"),
    ]
)
def test_get_current_zone_residual_heat_state(hb_appliance, zone_key, expected_value):
    assert hb_appliance.get_current_zone_residual_heat_state(zone_key) == expected_value


@pytest.mark.parametrize(
    "zone_key,expected_value",
    [
        ("hobZone1", 0),
        ("hobZone2", 0),
        ("hobZone3", 0),
        ("hobZone4", 0),
    ]
)
def test_get_current_zone_target_duration(hb_appliance, zone_key, expected_value):
    assert hb_appliance.get_current_zone_target_duration(zone_key) == expected_value


@pytest.mark.parametrize(
    "zone_key,expected_value",
    [
        ("hobZone1", -1),
        ("hobZone2", -1),
        ("hobZone3", -1),
        ("hobZone4", -1),
    ]
)
def test_get_current_zone_reminder_time(hb_appliance, zone_key, expected_value):
    assert hb_appliance.get_current_zone_reminder_time(zone_key) == expected_value


@pytest.mark.parametrize(
    "zone_key,expected_value",
    [
        ("hobZone1", "NO_POT_IDLE"),
        ("hobZone2", "NO_POT_IDLE"),
        ("hobZone3", "NO_POT_IDLE"),
        ("hobZone4", "NO_POT_IDLE"),
    ]
)
def test_get_current_zone_hob_pot_detected(hb_appliance, zone_key, expected_value):
    assert hb_appliance.get_current_zone_hob_pot_detected(zone_key) == expected_value


def test_get_hood_fan_speed_command(hb_appliance):
    cmd = hb_appliance.get_hood_fan_speed_command("BOOST")
    assert cmd == {"hobHood": {"hobToHoodFanSpeed": "BOOST"}}


def test_get_hood_state_command(hb_appliance):
    cmd = hb_appliance.get_hood_state_command("MANUAL")
    assert cmd == {"hobHood": {"hobToHoodState": "MANUAL"}}


def test_get_key_sound_tone_command(hb_appliance):
    cmd = hb_appliance.get_key_sound_tone_command("CLICK")
    assert cmd == {"keySoundTone": "CLICK"}


def test_get_enable_child_lock_command(hb_appliance):
    cmd = hb_appliance.get_enable_child_lock_command()
    assert cmd == {"childLock": True}
