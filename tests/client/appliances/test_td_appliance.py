import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest
from freezegun import freeze_time

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.td_appliance import TDAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import PROGRAM_CAPABILITY


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def td_appliance() -> TDAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "td_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyTD",
        applianceType="TD",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "td_state.json")

    return cast(TDAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(td_appliance):
    assert td_appliance.is_feature_supported(PROGRAM_CAPABILITY) is True


def test_is_feature_supported_false(td_appliance):
    assert td_appliance.is_feature_supported("invalid_cap") is False


def test_get_supported_programs(td_appliance):
    assert td_appliance.get_supported_programs() == ['AUTO_EASY_IRON_PR_EASYIRON_TD',
                                                     'BABY_PR_BABY',
                                                     'BED_LINEN_PLUS_PR_BEDLINENPLUSITA',
                                                     'COTTON_PR_COTTONS',
                                                     'COTTON_PR_COTTONSECO',
                                                     'CURTAINS_PR_CURTAINS',
                                                     'DOWN_JACKET_PR_DOWN_JACKET',
                                                     'DRY_CLEANING_PR_REFRESH',
                                                     'DUVET_PR_DUVET',
                                                     'EXTRA_DELICATE_PR_DELICATES',
                                                     'HYGIENE_PR_HYGIENE',
                                                     'JEANS_PR_DENIM',
                                                     'LINEN_PR_LINEN',
                                                     'MY_DRY_PR_MIXDRY',
                                                     'NA_ALLERGEN_PR_ALLERGEN',
                                                     'OUTD_PROOF_PR_OUTDOOR',
                                                     'PETBED_PR_PETHAIR',
                                                     'PILLOWS_PR_PILLOW',
                                                     'QUICK_PR_QUICK_3KG',
                                                     'SHOES_PR_RUNNINGSHOES',
                                                     'SILK_DRY_PR_SILK',
                                                     'SKIING_PR_SKIINGGEAR',
                                                     'SOCCER_RUGBY_PR_SOCCER_RUGBY',
                                                     'SPORTWEAR_PR_SPORTWEAR',
                                                     'SYNTHETIC_PR_SYNTHETICS',
                                                     'TIMEDRY_PR_DRYINGRACK',
                                                     'TOWELS_PR_TOWELS',
                                                     'TRAINING_GEAR_PR_DAILYTRAINING',
                                                     'WOOL_GOLD_PR_WOOL']


def test_get_current_program(td_appliance):
    assert td_appliance.get_current_program() == "COTTON_PR_COTTONS"


def test_get_current_cycle_phase(td_appliance):
    assert td_appliance.get_current_cycle_phase() == "UNAVAILABLE"


def test_get_current_time_to_end(td_appliance):
    assert td_appliance.get_current_time_to_end() == 10440


def test_get_current_appliance_state(td_appliance):
    assert td_appliance.get_current_appliance_state() == "DELAYED_START"


def test_get_start_command(td_appliance):
    cmd = td_appliance.get_start_command()
    assert cmd == {"executeCommand": "START"}


def test_get_stop_command(td_appliance):
    cmd = td_appliance.get_stop_command()
    assert cmd == {"executeCommand": "STOPRESET"}


def test_get_resume_command(td_appliance):
    cmd = td_appliance.get_resume_command()
    assert cmd == {"executeCommand": "RESUME"}


def test_get_pause_command(td_appliance):
    cmd = td_appliance.get_pause_command()
    assert cmd == {"executeCommand": "PAUSE"}


def test_get_set_program_command(td_appliance):
    cmd = td_appliance.get_set_program_command("COTTON_PR_COTTONS")
    assert cmd == {"userSelections": {"programUID": "COTTON_PR_COTTONS"}}


def test_get_current_door_state(td_appliance):
    assert td_appliance.get_current_door_state() == "OPEN"


def test_get_current_remote_control(td_appliance):
    assert td_appliance.get_current_remote_control() == "NOT_SAFETY_RELEVANT_ENABLED"


def test_get_current_water_hardness(td_appliance):
    assert td_appliance.get_current_water_hardness() == "SOFT"


def test_get_current_ui_lock_mode(td_appliance):
    assert td_appliance.get_current_ui_lock_mode() == False


def test_get_current_alerts(td_appliance):
    assert td_appliance.get_current_alerts() == [{
        "severity": "WARNING",
        "acknowledgeStatus": "PENDING",
        "code": "POWER_FAILURE"
    }]


@freeze_time("2025-07-21 14:00:00")
def test_get_current_start_at(td_appliance):
    start_at = td_appliance.get_current_start_at()
    assert start_at.isoformat() == "2025-07-21T14:30:00+00:00"


@freeze_time("2025-07-21 14:00:00")
def test_get_current_end_at(td_appliance):
    end_at = td_appliance.get_current_end_at()
    assert end_at.isoformat() == "2025-07-21T17:24:00+00:00"
