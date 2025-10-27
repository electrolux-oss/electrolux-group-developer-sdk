import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.cr_appliance import CRAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import AIR_FILTER_STATE, APPLIANCE_STATE


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def cr_appliance() -> CRAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "cr_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyCR",
        applianceType="CR",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "cr_state.json")

    return cast(CRAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(cr_appliance):
    assert cr_appliance.is_feature_supported(AIR_FILTER_STATE) is True


def test_is_feature_supported_false(cr_appliance):
    assert cr_appliance.is_feature_supported("invalid_cap") is False


def test_is_cavity_feature_supported_true(cr_appliance):
    assert cr_appliance.is_cavity_feature_supported("extraCavity", APPLIANCE_STATE) is True


def test_is_cavity_feature_supported_false(cr_appliance):
    assert cr_appliance.is_cavity_feature_supported("invalid_cavity", APPLIANCE_STATE) is False


def test_get_supported_cavities(cr_appliance):
    assert cr_appliance.get_supported_cavities() == ['fridge', 'iceMaker', 'extraCavity', 'freezer']


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("fridge", 1.0),
        ("freezer", -23.0),
    ]
)
def test_get_supported_min_temperature(cr_appliance, cavity, expected_result):
    assert cr_appliance.get_supported_min_temperature(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("fridge", 7.0),
        ("freezer", -13.0),
    ]
)
def test_get_supported_max_temperature(cr_appliance, cavity, expected_result):
    assert cr_appliance.get_supported_max_temperature(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("fridge", 1.0),
        ("freezer", 1.0),
    ]
)
def test_get_supported_step_temperature(cr_appliance, cavity, expected_result):
    assert cr_appliance.get_supported_step_temperature(cavity) == expected_result


def test_get_supported_extra_cavity_temperature(cr_appliance):
    assert cr_appliance.get_supported_extra_cavity_temperature() == [-2.0,
                                                                     0.0,
                                                                     3.0,
                                                                     7.0]


def test_get_current_temperature_unit(cr_appliance):
    assert cr_appliance.get_current_temperature_unit() == "CELSIUS"


def test_get_current_alerts(cr_appliance):
    assert cr_appliance.get_current_alerts() == []


def test_get_current_ui_lock_mode(cr_appliance):
    assert cr_appliance.get_current_ui_lock_mode() == False


def test_get_current_water_filter_state(cr_appliance):
    assert cr_appliance.get_current_water_filter_state() == "GOOD"


def test_get_current_air_filter_state(cr_appliance):
    assert cr_appliance.get_current_air_filter_state() == "BUY"


def test_get_current_vacation_holiday_mode(cr_appliance):
    assert cr_appliance.get_current_vacation_holiday_mode() == "OFF"


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("fridge", 4.0),
        ("freezer", -18.0),
        ("extraCavity", 3.5)
    ]
)
def test_get_current_cavity_target_temperature_c(cr_appliance, cavity, expected_result):
    assert cr_appliance.get_current_cavity_target_temperature_c(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("fridge", 39.2),
        ("freezer", -0.3999999999999986),
        ("extraCavity", 38.3)
    ]
)
def test_get_current_cavity_target_temperature_f(cr_appliance, cavity, expected_result):
    assert cr_appliance.get_current_cavity_target_temperature_f(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("fridge", "RUNNING"),
        ("freezer", "RUNNING"),
        ("extraCavity", "RUNNING"),
        ("iceMaker", "RUNNING")
    ]
)
def test_get_current_cavity_appliance_state(cr_appliance, cavity, expected_result):
    assert cr_appliance.get_current_cavity_appliance_state(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("fridge", []),
        ("freezer", []),
        ("extraCavity", []),
        ("iceMaker", [])
    ]
)
def test_get_current_cavity_alerts(cr_appliance, cavity, expected_result):
    assert cr_appliance.get_current_cavity_alerts(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, expected_result",
    [
        ("fridge", "CLOSED"),
        ("freezer", "CLOSED"),
        ("extraCavity", "CLOSED")
    ]
)
def test_get_current_cavity_door_state(cr_appliance, cavity, expected_result):
    assert cr_appliance.get_current_cavity_door_state(cavity) == expected_result


@pytest.mark.parametrize(
    "cavity, temperature",
    [
        ("fridge", 41.0),
        ("freezer", 3.2),
        ("extraCavity", 95)
    ]
)
def test_get_set_cavity_temperature_f_command(cr_appliance, cavity, temperature):
    assert cr_appliance.get_set_cavity_temperature_f_command(cavity, temperature) == {
        cavity: {"targetTemperatureF": temperature}
    }


@pytest.mark.parametrize(
    "cavity, temperature",
    [
        ("fridge", 5.0),
        ("freezer", -16),
        ("extraCavity", 3.5)
    ]
)
def test_get_set_cavity_temperature_c_command(cr_appliance, cavity, temperature):
    assert cr_appliance.get_set_cavity_temperature_c_command(cavity, temperature) == {
        cavity: {"targetTemperatureC": temperature}
    }


def test_get_set_vacation_holiday_mode_command(cr_appliance):
    assert cr_appliance.get_set_vacation_holiday_mode_command("OFF") == {"vacationHolidayMode": "OFF"}
