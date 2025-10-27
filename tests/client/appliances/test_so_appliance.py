import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest
from freezegun import freeze_time

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.so_appliance import SOAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import REMOTE_CONTROL, APPLIANCE_STATE


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def so_appliance() -> SOAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "so_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MySO",
        applianceType="SO",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "so_state.json")

    return cast(SOAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(so_appliance):
    assert so_appliance.is_feature_supported(REMOTE_CONTROL) is True


def test_is_feature_supported_false(so_appliance):
    assert so_appliance.is_feature_supported("invalid_cap") is False


def test_is_cavity_feature_supported_true(so_appliance):
    assert so_appliance.is_cavity_feature_supported("bottomOven", APPLIANCE_STATE) is True


def test_is_cavity_feature_supported_false(so_appliance):
    assert so_appliance.is_cavity_feature_supported("invalid_cavity", APPLIANCE_STATE) is False


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", ['AIR_FRY',
                        'BAKE',
                        'CONVENTIONAL_BAKE',
                        'CONVENTIONAL_ROAST',
                        'KEEP_WARM',
                        'PRE_HEAT']),
        ("upperOven", ['AIR_FRY',
                       'BAKE',
                       'CONVENTIONAL_BAKE',
                       'CONVENTIONAL_ROAST',
                       'KEEP_WARM',
                       'PRE_HEAT'])
    ]
)
def test_get_cavity_supported_programs(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_programs(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 170.0),
        ("upperOven", 170.0)
    ]
)
def test_get_cavity_supported_min_temp(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_min_temp(cavity, "BAKE") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 170.0),
        ("upperOven", 170.0)
    ]
)
def test_get_cavity_supported_min_temp_unknown_program(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_min_temp(cavity, "UNKNOWN") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 550.0),
        ("upperOven", 550.0)
    ]
)
def test_get_cavity_supported_max_temp(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_max_temp(cavity, "BAKE") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 550.0),
        ("upperOven", 550.0)
    ]
)
def test_get_cavity_supported_max_temp_unknown_program(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_max_temp(cavity, "UNKNOWN") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 5.0),
        ("upperOven", 5.0)
    ]
)
def test_get_cavity_supported_step_temp(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_step_temp(cavity, "BAKE") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 1.0),
        ("upperOven", 1.0)
    ]
)
def test_get_cavity_supported_step_temp_unknown_program(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_step_temp(cavity, "UNKNOWN") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 60),
        ("upperOven", 60)
    ]
)
def test_get_cavity_supported_min_duration(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_min_duration(cavity, "BAKE") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 60),
        ("upperOven", 60)
    ]
)
def test_get_cavity_supported_min_duration_unknown_program(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_min_duration(cavity, "UNKNOWN") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 43140),
        ("upperOven", 43140)
    ]
)
def test_get_cavity_supported_max_duration(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_max_duration(cavity, "BAKE") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 43140),
        ("upperOven", 43140)
    ]
)
def test_get_cavity_supported_max_duration_unknown_program(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_max_duration(cavity, "UNKNOWN") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 60),
        ("upperOven", 60)
    ]
)
def test_get_cavity_supported_step_duration(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_step_duration(cavity, "BAKE") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 60),
        ("upperOven", 60)
    ]
)
def test_get_cavity_supported_step_duration_unknown_program(so_appliance, cavity, expected_result):
    assert so_appliance.get_cavity_supported_step_duration(cavity, "UNKNOWN") == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", "BAKE"),
        ("upperOven", "KEY_ERROR")
    ]
)
def test_get_current_cavity_program(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_program(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", "RUNNING"),
        ("upperOven", "DELAYED_START")
    ]
)
def test_get_current_cavity_appliance_state(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_appliance_state(cavity) == expected_result


def test_get_current_temperature_unit(so_appliance):
    assert so_appliance.get_current_temperature_unit() == "FAHRENHEIT"


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 176.67),
        ("upperOven", -17.77777777777778)
    ]
)
def test_get_current_cavity_target_temperature_c(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_target_temperature_c(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 350.0),
        ("upperOven", 0.0)
    ]
)
def test_get_current_cavity_target_temperature_f(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_target_temperature_f(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 37.77777777777778),
        ("upperOven", None)
    ]
)
def test_get_current_cavity_display_temperature_c(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_display_temperature_c(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 100.0),
        ("upperOven", None)
    ]
)
def test_get_current_cavity_display_temperature_f(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_display_temperature_f(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", False),
        ("upperOven", False)
    ]
)
def test_get_current_cavity_cavity_light(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_cavity_light(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", "NOT_INSERTED"),
        ("upperOven", "NOT_INSERTED")
    ]
)
def test_get_current_cavity_food_probe_insertion_state(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_food_probe_insertion_state(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", None),
        ("upperOven", None)
    ]
)
def test_get_current_cavity_display_food_probe_temperature_f(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_display_food_probe_temperature_f(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", None),
        ("upperOven", None)
    ]
)
def test_get_current_cavity_display_food_probe_temperature_c(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_display_food_probe_temperature_c(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", "CLOSED"),
        ("upperOven", "CLOSED")
    ]
)
def test_get_current_cavity_door_state(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_door_state(cavity) == expected_result


def test_get_current_remote_control(so_appliance):
    assert so_appliance.get_current_remote_control() == "ENABLED"


def test_get_current_alerts(so_appliance):
    assert so_appliance.get_current_alerts() == [{'acknowledgeStatus': 'NOT_NEEDED', 'code': '36', 'severity': 'FAULT'}]


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", None),
        ("upperOven", None)
    ]
)
def test_get_current_cavity_running_time(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_running_time(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 60),
        ("upperOven", 0)
    ]
)
def test_get_current_cavity_time_to_end(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_time_to_end(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("bottomOven", 120),
        ("upperOven", 0)
    ]
)
def test_get_current_cavity_target_duration(so_appliance, cavity, expected_result):
    assert so_appliance.get_current_cavity_target_duration(cavity) == expected_result


@freeze_time("2025-07-22 14:00:00")
def test_get_current_cavity_upper_oven_start_at(so_appliance):
    start_at = so_appliance.get_current_cavity_start_at("upperOven")
    assert start_at.isoformat() == "2025-07-22T15:00:00+00:00"


def test_get_current_cavity_bottom_oven_start_at(so_appliance):
    start_at = so_appliance.get_current_cavity_start_at("bottomOven")
    assert start_at is None


@pytest.mark.parametrize(
    "cavity",
    [
        "bottomOven",
        "upperOven"
    ]
)
def test_get_program_command(so_appliance, cavity):
    assert so_appliance.get_program_command(cavity, "BAKE") == {cavity: {"program": "BAKE"}}


@pytest.mark.parametrize(
    "cavity",
    [
        "bottomOven",
        "upperOven"
    ]
)
def test_get_cavity_light_command(so_appliance, cavity):
    assert so_appliance.get_cavity_light_command(cavity, True) == {cavity: {"cavityLight": True}}


@pytest.mark.parametrize(
    "cavity",
    [
        "bottomOven",
        "upperOven"
    ]
)
def test_get_temperature_c_command(so_appliance, cavity):
    assert so_appliance.get_temperature_c_command(cavity, 180.0) == {cavity: {"targetTemperatureC": 180.0}}


@pytest.mark.parametrize(
    "cavity",
    [
        "bottomOven",
        "upperOven"
    ]
)
def test_get_temperature_f_command(so_appliance, cavity):
    assert so_appliance.get_temperature_f_command(cavity, 356.0) == {cavity: {"targetTemperatureF": 356.0}}


@pytest.mark.parametrize(
    "cavity",
    [
        "bottomOven",
        "upperOven"
    ]
)
def test_get_target_duration_command(so_appliance, cavity):
    assert so_appliance.get_target_duration_command(cavity, 3600) == {cavity: {"targetDuration": 3600}}


@pytest.mark.parametrize(
    "cavity",
    [
        "bottomOven",
        "upperOven"
    ]
)
def test_get_start_command(so_appliance, cavity):
    assert so_appliance.get_start_command(cavity) == {cavity: {"executeCommand": "START"}}


@pytest.mark.parametrize(
    "cavity",
    [
        "bottomOven",
        "upperOven"
    ]
)
def test_get_stop_command(so_appliance, cavity):
    assert so_appliance.get_stop_command(cavity) == {cavity: {"executeCommand": "STOPRESET"}}
