import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest
from freezegun import freeze_time

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.wd_appliance import WDAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import TANK_B_DET_LOAD_FOR_NOMINAL_WEIGHT_CAPABILITY, \
    AD_TANK_B_DET_LOADED_CAPABILITY


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def wd_appliance() -> WDAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "wd_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyWD",
        applianceType="WD",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "wd_state.json")

    return cast(WDAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(wd_appliance):
    assert wd_appliance.is_feature_supported(TANK_B_DET_LOAD_FOR_NOMINAL_WEIGHT_CAPABILITY) is True


def test_is_feature_supported_false(wd_appliance):
    assert wd_appliance.is_feature_supported(AD_TANK_B_DET_LOADED_CAPABILITY) is False


def test_get_supported_programs(wd_appliance):
    assert wd_appliance.get_supported_programs() == ['BABY_PR_BABY_WM_WD',
                                                     'BEDLINEN_XL_PR_BEDLINENXL',
                                                     'BLANKET_PR_DUVET',
                                                     'COTTON_PR_COTTONS',
                                                     'COTTON_PR_ECO40-60',
                                                     'DELICATE_PR_DELICATES',
                                                     'DENIM_PR_DENIM',
                                                     'DRUM_CLEAN_PR_MACHINECLEAN',
                                                     'EXPRESS_PR_BUSINESSSHIRT',
                                                     'EXPRESS_PR_MIXLOAD',
                                                     'LINEN_PR_LINEN_WM_WD',
                                                     'ONE_ITEM_FAST_PR_1ITEMFAST',
                                                     'PET_HAIR_PR_PETHAIR',
                                                     'QUICK_WASH_DRY_PR_QUICK20WASH_DRY60',
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
                                                     'SYNTHETIC_PR_EASYIRON',
                                                     'SYNTHETIC_PR_SYNTHETICS',
                                                     'TOWELS_PR_TOWELS_BASE',
                                                     'TRAINING_GEAR_PR_DAILYTRAINING',
                                                     'WOOL_PR_WOOL_HANDWASH']


def test_get_supported_spin_speeds(wd_appliance):
    assert wd_appliance.get_supported_spin_speeds() == ['1000_RPM',
                                                        '1200_RPM',
                                                        '1400_RPM',
                                                        '1600_RPM',
                                                        '400_RPM',
                                                        '600_RPM',
                                                        '800_RPM']


def test_get_supported_temperature(wd_appliance):
    assert wd_appliance.get_supported_temperature() == [
        '40_CELSIUS']


def test_get_current_program(wd_appliance):
    assert wd_appliance.get_current_program() == "COTTON_PR_ECO40-60"


def test_get_current_cycle_phase(wd_appliance):
    assert wd_appliance.get_current_cycle_phase() == "UNAVAILABLE"


def test_get_current_time_to_end(wd_appliance):
    assert wd_appliance.get_current_time_to_end() == 5400


def test_get_current_appliance_state(wd_appliance):
    assert wd_appliance.get_current_appliance_state() == "DELAYED_START"


def test_get_current_spin_speed(wd_appliance):
    assert wd_appliance.get_current_spin_speeds() == "1600_RPM"


def test_get_current_temperature(wd_appliance):
    assert wd_appliance.get_current_temperature() == "40_CELSIUS"


def test_get_start_command(wd_appliance):
    cmd = wd_appliance.get_start_command()
    assert cmd == {"executeCommand": "START"}


def test_get_stop_command(wd_appliance):
    cmd = wd_appliance.get_stop_command()
    assert cmd == {"executeCommand": "STOPRESET"}


def test_get_resume_command(wd_appliance):
    cmd = wd_appliance.get_resume_command()
    assert cmd == {"executeCommand": "RESUME"}


def test_get_pause_command(wd_appliance):
    cmd = wd_appliance.get_pause_command()
    assert cmd == {"executeCommand": "PAUSE"}


def test_get_set_program_command(wd_appliance):
    cmd = wd_appliance.get_set_program_command("COTTON_PR_COTTONS")
    assert cmd == {"userSelections": {"programUID": "COTTON_PR_COTTONS"}}


def test_get_set_spin_speed_command(wd_appliance):
    cmd = wd_appliance.get_set_spin_speed_command("600_RPM")
    assert cmd == {"userSelections": {"programUID": "COTTON_PR_ECO40-60", "analogSpinSpeed": "600_RPM"}}


def test_get_set_spin_speed_command_program_in_args(wd_appliance):
    cmd = wd_appliance.get_set_spin_speed_command("600_RPM", "COTTON_PR_COTTONS")
    assert cmd == {"userSelections": {"programUID": "COTTON_PR_COTTONS", "analogSpinSpeed": "600_RPM"}}


def test_get_set_temperature_command(wd_appliance):
    cmd = wd_appliance.get_set_temperature_command("20_CELSIUS")
    assert cmd == {"userSelections": {"programUID": "COTTON_PR_ECO40-60", "analogTemperature": "20_CELSIUS"}}


def test_get_set_temperature_command_program_in_args(wd_appliance):
    cmd = wd_appliance.get_set_temperature_command("20_CELSIUS", "COTTON_PR_COTTONS")
    assert cmd == {"userSelections": {"programUID": "COTTON_PR_COTTONS", "analogTemperature": "20_CELSIUS"}}


def test_get_current_door_state(wd_appliance):
    assert wd_appliance.get_current_door_state() == "CLOSED"


def test_get_current_remote_control(wd_appliance):
    assert wd_appliance.get_current_remote_control() == "NOT_SAFETY_RELEVANT_ENABLED"


def test_get_current_water_hardness(wd_appliance):
    assert wd_appliance.get_current_water_hardness() == "STEP_4"


def test_get_current_ui_lock_mode(wd_appliance):
    assert wd_appliance.get_current_ui_lock_mode() == False


def test_get_current_alerts(wd_appliance):
    assert wd_appliance.get_current_alerts() == [{
        "severity": "WARNING",
        "acknowledgeStatus": "PENDING",
        "code": "DETERGENT_OVERDOSING"
    }]


def test_get_current_f_c_miscellaneous_state_water_usage(wd_appliance):
    assert wd_appliance.get_current_f_c_miscellaneous_state_water_usage() == 0


def test_get_current_f_c_miscellaneous_state_ad_tank_b_det_loaded(wd_appliance):
    assert wd_appliance.get_current_f_c_miscellaneous_state_ad_tank_b_det_loaded() is None


def test_get_current_f_c_miscellaneous_state_tank_a_det_load_for_nominal_weight(wd_appliance):
    assert wd_appliance.get_current_f_c_miscellaneous_state_tank_a_det_load_for_nominal_weight() == 0


def test_get_current_f_c_miscellaneous_state_optisense_result(wd_appliance):
    assert wd_appliance.get_current_f_c_miscellaneous_state_optisense_result() == 0


def test_get_current_f_c_miscellaneous_state_ad_tank_b_soft_loaded(wd_appliance):
    assert wd_appliance.get_current_f_c_miscellaneous_state_ad_tank_b_soft_loaded() is None


def test_get_current_f_c_miscellaneous_state_eco_level(wd_appliance):
    assert wd_appliance.get_current_f_c_miscellaneous_state_eco_level() == 6


def test_get_current_f_c_miscellaneous_state_ad_tank_a_det_loaded(wd_appliance):
    assert wd_appliance.get_current_f_c_miscellaneous_state_ad_tank_a_det_loaded() is None


def test_get_current_f_c_miscellaneous_state_tank_b_det_load_for_nominal_weight(wd_appliance):
    assert wd_appliance.get_current_f_c_miscellaneous_state_tank_b_det_load_for_nominal_weight() == 78


def test_get_current_f_c_miscellaneous_state_tank_a_reserve(wd_appliance):
    assert wd_appliance.get_current_f_c_miscellaneous_state_tank_a_reserve() == False


def test_get_current_f_c_miscellaneous_state_tank_b_reserve(wd_appliance):
    assert wd_appliance.get_current_f_c_miscellaneous_state_tank_b_reserve() == False


@freeze_time("2025-07-21 14:00:00")
def test_get_current_start_at(wd_appliance):
    start_at = wd_appliance.get_current_start_at()
    assert start_at.isoformat() == "2025-07-21T15:00:00+00:00"


@freeze_time("2025-07-21 14:00:00")
def test_get_current_end_at(wd_appliance):
    end_at = wd_appliance.get_current_end_at()
    assert end_at.isoformat() == "2025-07-21T16:30:00+00:00"
