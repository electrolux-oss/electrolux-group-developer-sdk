import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest
from freezegun import freeze_time

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.ov_appliance import OVAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import PROGRAM


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def ov_appliance() -> OVAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "ov_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyOV",
        applianceType="OV",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "ov_state.json")

    return cast(OVAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(ov_appliance):
    assert ov_appliance.is_feature_supported(PROGRAM) is True


def test_is_feature_supported_false(ov_appliance):
    assert ov_appliance.is_feature_supported("invalid_cap") is False


def test_get_supported_programs(ov_appliance):
    assert ov_appliance.get_supported_programs() == ['AUGRATIN',
                                                     'BOTTOM',
                                                     'BREAD_BAKING',
                                                     'CONVENTIONAL_COOKING',
                                                     'DOUGH_PROVING',
                                                     'DRYING',
                                                     'FROZEN_FOOD',
                                                     'GRILL',
                                                     'GRILL_FAN',
                                                     'KEEP_WARM',
                                                     'PIZZA',
                                                     'PLATE_WARMING',
                                                     'PRESERVING',
                                                     'SLOW_COOK',
                                                     'TRUE_FAN']


def test_get_supported_min_temp(ov_appliance):
    assert ov_appliance.get_supported_min_temp("PIZZA") == 80.0


def test_get_supported_min_temp_unknown_program(ov_appliance):
    assert ov_appliance.get_supported_min_temp("UNKNOWN") == 0.0


def test_get_supported_max_temp(ov_appliance):
    assert ov_appliance.get_supported_max_temp("PIZZA") == 230.0


def test_get_supported_max_temp_unknown_program(ov_appliance):
    assert ov_appliance.get_supported_max_temp("UNKNOWN") == 350.0


def test_get_supported_step_temp(ov_appliance):
    assert ov_appliance.get_supported_step_temp("PIZZA") == 5.0


def test_get_supported_step_temp_unknown_program(ov_appliance):
    assert ov_appliance.get_supported_step_temp("UNKNOWN") == 5.0


def test_get_supported_min_duration(ov_appliance):
    assert ov_appliance.get_supported_min_duration("PIZZA") == 0


def test_get_supported_min_duration_unknown_program(ov_appliance):
    assert ov_appliance.get_supported_min_duration("UNKNOWN") == 0


def test_get_supported_max_duration(ov_appliance):
    assert ov_appliance.get_supported_max_duration("PIZZA") == 86340


def test_get_supported_max_duration_unknown_program(ov_appliance):
    assert ov_appliance.get_supported_max_duration("UNKNOWN") == 86340


def test_get_supported_step_duration(ov_appliance):
    assert ov_appliance.get_supported_step_duration("PIZZA") == 60


def test_get_supported_step_duration_unknown_program(ov_appliance):
    assert ov_appliance.get_supported_step_duration("UNKNOWN") == 60


def test_get_current_program(ov_appliance):
    assert ov_appliance.get_current_program() == "TRUE_FAN"


def test_get_current_appliance_state(ov_appliance):
    assert ov_appliance.get_current_appliance_state() == "DELAYED_START"


def test_get_current_temperature_unit(ov_appliance):
    assert ov_appliance.get_current_temperature_unit() == "CELSIUS"


def test_get_current_target_temperature_c(ov_appliance):
    assert ov_appliance.get_current_target_temperature_c() == 150.0


def test_get_current_target_temperature_f(ov_appliance):
    assert ov_appliance.get_current_target_temperature_f() == 302.0


def test_get_current_display_temperature_c(ov_appliance):
    assert ov_appliance.get_current_display_temperature_c() == 130.0


def test_get_current_display_temperature_f(ov_appliance):
    assert ov_appliance.get_current_display_temperature_f() == 266.0


def test_get_current_cavity_light(ov_appliance):
    assert ov_appliance.get_current_cavity_light() == False


def test_get_current_food_probe_insertion_state(ov_appliance):
    assert ov_appliance.get_current_food_probe_insertion_state() == "NOT_INSERTED"


def test_get_current_display_food_probe_temperature_f(ov_appliance):
    assert ov_appliance.get_current_display_food_probe_temperature_f() == 32


def test_get_current_display_food_probe_temperature_c(ov_appliance):
    assert ov_appliance.get_current_display_food_probe_temperature_c() == 0


def test_get_current_door_state(ov_appliance):
    assert ov_appliance.get_current_door_state() == "CLOSED"


def test_get_current_remote_control(ov_appliance):
    assert ov_appliance.get_current_remote_control() == "ENABLED"


def test_get_current_alerts(ov_appliance):
    assert ov_appliance.get_current_alerts() == []


def test_get_current_running_time(ov_appliance):
    assert ov_appliance.get_current_running_time() == 0


def test_get_current_time_to_end(ov_appliance):
    assert ov_appliance.get_current_time_to_end() == 0


def test_get_current_target_duration(ov_appliance):
    assert ov_appliance.get_current_target_duration() == 0


@freeze_time("2025-07-22 14:00:00")
def test_get_current_start_at(ov_appliance):
    start_at = ov_appliance.get_current_start_at()
    assert start_at.isoformat() == "2025-07-22T14:30:00+00:00"


def test_get_program_command(ov_appliance):
    assert ov_appliance.get_program_command("PIZZA") == {
        "program": "PIZZA"
    }


def test_get_cavity_light_command(ov_appliance):
    assert ov_appliance.get_cavity_light_command(True) == {
        "cavityLight": True
    }


def test_get_temperature_c_command(ov_appliance):
    assert ov_appliance.get_temperature_c_command(180.0) == {
        "targetTemperatureC": 180.0
    }


def test_get_temperature_f_command(ov_appliance):
    assert ov_appliance.get_temperature_f_command(356.0) == {
        "targetTemperatureF": 356.0
    }


def test_get_target_duration_command(ov_appliance):
    assert ov_appliance.get_target_duration_command(3600) == {
        "targetDuration": 3600
    }


def test_get_start_command(ov_appliance):
    assert ov_appliance.get_start_command() == {
        "executeCommand": "START"
    }


def test_get_stop_command(ov_appliance):
    assert ov_appliance.get_stop_command() == {
        "executeCommand": "STOPRESET"
    }
