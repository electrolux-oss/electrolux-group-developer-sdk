import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest
from freezegun import freeze_time

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.wm_appliance import WMAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import TANK_B_DET_LOAD_FOR_NOMINAL_WEIGHT_CAPABILITY


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def wm_appliance() -> WMAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "wm_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyWM",
        applianceType="WM",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "wm_state.json")

    return cast(WMAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(wm_appliance):
    assert wm_appliance.is_feature_supported(TANK_B_DET_LOAD_FOR_NOMINAL_WEIGHT_CAPABILITY) is True


def test_is_feature_supported_false(wm_appliance):
    assert wm_appliance.is_feature_supported("invalid_cap") is False


def test_get_supported_programs(wm_appliance):
    assert wm_appliance.get_supported_programs() == ['BABY_PR_BABY_WM_WD',
                                                     'BEDLINEN_XL_PR_BEDLINENXL',
                                                     'BLANKET_PR_DUVET',
                                                     'BLANKET_PR_PILLOWS',
                                                     'COTTON_PR_COTTONS',
                                                     'COTTON_PR_ECO40-60',
                                                     'DELICATE_PR_CURTAINS',
                                                     'DELICATE_PR_DELICATES',
                                                     'DENIM_PR_DENIM',
                                                     'DRUM_CLEAN_PR_MACHINECLEAN',
                                                     'EXPRESS_PR_BUSINESSSHIRT',
                                                     'EXPRESS_PR_POWERCLEAN59MIN',
                                                     'LINEN_PR_LINEN_WM_WD',
                                                     'MINI_PR_SILK',
                                                     'ONE_ITEM_FAST_PR_1ITEMFAST',
                                                     'PET_HAIR_PR_PETHAIR',
                                                     'QUICK_20_MIN_PR_20MIN3KG',
                                                     'SANITISE60_PR_ANTIALLERGYVAPOUR',
                                                     'SANITISE60_PR_HYGIENE',
                                                     'SHOES_PR_RUNNINGSHOES',
                                                     'SOCCER_RUGBY_SOCCER_RUGBY',
                                                     'SOFTENER_PR_RINSE',
                                                     'SPIN_PR_DRAIN_SPIN',
                                                     'SPORTWEAR_PR_SPORTWEAR_WX',
                                                     'SPORT_JACKETS_PR_DOWN_JACKET',
                                                     'SPORT_JACKETS_PR_OUTDOOR',
                                                     'SPORT_JACKETS_PR_SKIING',
                                                     'STEAM_DEWRINKLER_PR_STEAMCASHMERE',
                                                     'STEAM_REFRESH_PR_STEAM',
                                                     'SYNTHETIC_PR_EASYIRON',
                                                     'SYNTHETIC_PR_SYNTHETICS',
                                                     'TOWELS_PR_TOWELS_BASE',
                                                     'TRAINING_GEAR_PR_DAILYTRAINING',
                                                     'WOOL_PR_WOOL']


def test_get_supported_spin_speeds(wm_appliance):
    assert wm_appliance.get_supported_spin_speeds() == ['1000_RPM', '1200_RPM', '400_RPM', '600_RPM', '800_RPM']


def test_get_supported_temperature(wm_appliance):
    assert wm_appliance.get_supported_temperature() == ['20_CELSIUS',
                                                        '30_CELSIUS',
                                                        '40_CELSIUS',
                                                        '50_CELSIUS',
                                                        '60_CELSIUS',
                                                        'COLD']


def test_get_current_program(wm_appliance):
    assert wm_appliance.get_current_program() == "SYNTHETIC_PR_SYNTHETICS"


def test_get_current_cycle_phase(wm_appliance):
    assert wm_appliance.get_current_cycle_phase() == "UNAVAILABLE"


def test_get_current_time_to_end(wm_appliance):
    assert wm_appliance.get_current_time_to_end() == 1800


def test_get_current_appliance_state(wm_appliance):
    assert wm_appliance.get_current_appliance_state() == "DELAYED_START"


def test_get_current_spin_speed(wm_appliance):
    assert wm_appliance.get_current_spin_speeds() == "1200_RPM"


def test_get_current_temperature(wm_appliance):
    assert wm_appliance.get_current_temperature() == "40_CELSIUS"


def test_get_start_command(wm_appliance):
    cmd = wm_appliance.get_start_command()
    assert cmd == {"executeCommand": "START"}


def test_get_stop_command(wm_appliance):
    cmd = wm_appliance.get_stop_command()
    assert cmd == {"executeCommand": "STOPRESET"}


def test_get_resume_command(wm_appliance):
    cmd = wm_appliance.get_resume_command()
    assert cmd == {"executeCommand": "RESUME"}


def test_get_pause_command(wm_appliance):
    cmd = wm_appliance.get_pause_command()
    assert cmd == {"executeCommand": "PAUSE"}


def test_get_set_program_command(wm_appliance):
    cmd = wm_appliance.get_set_program_command("COTTON_PR_COTTONS")
    assert cmd == {"userSelections": {"programUID": "COTTON_PR_COTTONS"}}


def test_get_set_spin_speed_command(wm_appliance):
    cmd = wm_appliance.get_set_spin_speed_command("600_RPM")
    assert cmd == {"userSelections": {"programUID": "SYNTHETIC_PR_SYNTHETICS", "analogSpinSpeed": "600_RPM"}}


def test_get_set_spin_speed_command_program_in_args(wm_appliance):
    cmd = wm_appliance.get_set_spin_speed_command("600_RPM", "COTTON_PR_COTTONS")
    assert cmd == {"userSelections": {"programUID": "COTTON_PR_COTTONS", "analogSpinSpeed": "600_RPM"}}


def test_get_set_temperature_command(wm_appliance):
    cmd = wm_appliance.get_set_temperature_command("20_CELSIUS")
    assert cmd == {"userSelections": {"programUID": "SYNTHETIC_PR_SYNTHETICS", "analogTemperature": "20_CELSIUS"}}


def test_get_set_temperature_command_program_in_args(wm_appliance):
    cmd = wm_appliance.get_set_temperature_command("20_CELSIUS", "COTTON_PR_COTTONS")
    assert cmd == {"userSelections": {"programUID": "COTTON_PR_COTTONS", "analogTemperature": "20_CELSIUS"}}


def test_get_current_door_state(wm_appliance):
    assert wm_appliance.get_current_door_state() == "CLOSED"


def test_get_current_remote_control(wm_appliance):
    assert wm_appliance.get_current_remote_control() == "NOT_SAFETY_RELEVANT_ENABLED"


def test_get_current_water_hardness(wm_appliance):
    assert wm_appliance.get_current_water_hardness() == "STEP_4"


def test_get_current_ui_lock_mode(wm_appliance):
    assert wm_appliance.get_current_ui_lock_mode() == False


def test_get_current_alerts(wm_appliance):
    assert wm_appliance.get_current_alerts() == []


def test_get_current_f_c_miscellaneous_state_water_usage(wm_appliance):
    assert wm_appliance.get_current_f_c_miscellaneous_state_water_usage() == 0


def test_get_current_f_c_miscellaneous_state_ad_tank_b_det_loaded(wm_appliance):
    assert wm_appliance.get_current_f_c_miscellaneous_state_ad_tank_b_det_loaded() == 0


def test_get_current_f_c_miscellaneous_state_tank_a_det_load_for_nominal_weight(wm_appliance):
    assert wm_appliance.get_current_f_c_miscellaneous_state_tank_a_det_load_for_nominal_weight() == 0


def test_get_current_f_c_miscellaneous_state_ad_tank_b_soft_loaded(wm_appliance):
    assert wm_appliance.get_current_f_c_miscellaneous_state_ad_tank_b_soft_loaded() == 0


def test_get_current_f_c_miscellaneous_state_eco_level(wm_appliance):
    assert wm_appliance.get_current_f_c_miscellaneous_state_eco_level() == 255


def test_get_current_f_c_miscellaneous_state_ad_tank_a_det_loaded(wm_appliance):
    assert wm_appliance.get_current_f_c_miscellaneous_state_ad_tank_a_det_loaded() == 0


def test_get_current_f_c_miscellaneous_state_tank_b_det_load_for_nominal_weight(wm_appliance):
    assert wm_appliance.get_current_f_c_miscellaneous_state_tank_b_det_load_for_nominal_weight() == 0


def test_get_current_f_c_miscellaneous_state_tank_a_reserve(wm_appliance):
    assert wm_appliance.get_current_f_c_miscellaneous_state_tank_a_reserve() == False


def test_get_current_f_c_miscellaneous_state_tank_b_reserve(wm_appliance):
    assert wm_appliance.get_current_f_c_miscellaneous_state_tank_b_reserve() == False


@freeze_time("2025-07-21 14:00:00")
def test_get_current_start_at(wm_appliance):
    start_at = wm_appliance.get_current_start_at()
    assert start_at.isoformat() == "2025-07-21T17:30:00+00:00"


@freeze_time("2025-07-21 14:00:00")
def test_get_current_end_at(wm_appliance):
    end_at = wm_appliance.get_current_end_at()
    assert end_at.isoformat() == "2025-07-21T18:00:00+00:00"
