import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.dw_appliance import DWAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import PROGRAM_CAPABILITY


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def dw_appliance() -> DWAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "dw_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyDW",
        applianceType="DW",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "dw_state.json")

    return cast(DWAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(dw_appliance):
    assert dw_appliance.is_feature_supported(PROGRAM_CAPABILITY) is True


def test_is_feature_supported_false(dw_appliance):
    assert dw_appliance.is_feature_supported("invalid_cap") is False


def test_get_supported_programs(dw_appliance):
    assert dw_appliance.get_supported_programs() == ['AUTO',
                                                     'ECO',
                                                     'INTENSIVE',
                                                     'MACHINE_CARE',
                                                     'NORMAL90',
                                                     'QUICK30',
                                                     'QUICK60',
                                                     'RINSE']


def test_get_current_program(dw_appliance):
    assert dw_appliance.get_current_program() == "NORMAL90"


def test_get_current_cycle_phase(dw_appliance):
    assert dw_appliance.get_current_cycle_phase() == "UNAVAILABLE"


def test_get_current_time_to_end(dw_appliance):
    assert dw_appliance.get_current_time_to_end() == 8340


def test_get_current_appliance_state(dw_appliance):
    assert dw_appliance.get_current_appliance_state() == "OFF"


def test_get_start_command(dw_appliance):
    cmd = dw_appliance.get_start_command()
    assert cmd == {"executeCommand": "START"}


def test_get_stop_command(dw_appliance):
    cmd = dw_appliance.get_stop_command()
    assert cmd == {"executeCommand": "STOPRESET"}


def test_get_resume_command(dw_appliance):
    cmd = dw_appliance.get_resume_command()
    assert cmd == {"executeCommand": "RESUME"}


def test_get_pause_command(dw_appliance):
    cmd = dw_appliance.get_pause_command()
    assert cmd == {"executeCommand": "PAUSE"}


def test_get_set_program_command(dw_appliance):
    cmd = dw_appliance.get_set_program_command("ECO")
    assert cmd == {"userSelections": {"programUID": "ECO"}}


def test_get_current_door_state(dw_appliance):
    assert dw_appliance.get_current_door_state() == "OPEN"


def test_get_current_remote_control(dw_appliance):
    assert dw_appliance.get_current_remote_control() == "TEMPORARY_LOCKED"


def test_get_current_water_hardness(dw_appliance):
    assert dw_appliance.get_current_water_hardness() == "STEP_9"


def test_get_current_ui_lock_mode(dw_appliance):
    assert dw_appliance.get_current_ui_lock_mode() is None


def test_get_current_alerts(dw_appliance):
    assert dw_appliance.get_current_alerts() == [
        {
            "severity": "WARNING",
            "acknowledgeStatus": "NOT_NEEDED",
            "code": "DISH_ALARM_SALT_MISSING",
            "applianceCode": "101"
        },
        {
            "severity": "WARNING",
            "acknowledgeStatus": "NOT_NEEDED",
            "code": "DISH_ALARM_RINSE_AID_LOW",
            "applianceCode": "100"
        }]


def test_get_current_start_at(dw_appliance):
    start_at = dw_appliance.get_current_start_at()
    assert start_at is None


def test_get_current_end_at(dw_appliance):
    end_at = dw_appliance.get_current_end_at()
    assert end_at is None
