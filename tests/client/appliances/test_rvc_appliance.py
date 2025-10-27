import json
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from electrolux_group_developer_sdk.client.appliance_data_factory import appliance_data_factory
from electrolux_group_developer_sdk.client.appliances.rvc_appliance import RVCAppliance
from electrolux_group_developer_sdk.client.dto.appliance import Appliance
from electrolux_group_developer_sdk.feature_constants import MODE


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


@pytest.fixture
def rvc_appliance() -> RVCAppliance:
    details = load_json(Path(__file__).parent / "data" / "appliance" / "rvc_details.json")
    appliance = Appliance(
        applianceId="applianceId123",
        applianceName="MyRvc",
        applianceType="PUREi9",
        created=datetime.now()
    )
    state = load_json(Path(__file__).parent / "data" / "appliance" / "rvc_state.json")

    return cast(RVCAppliance, appliance_data_factory(
        appliance=appliance,
        details=details,
        state=state,
    ))


def test_is_feature_supported_true(rvc_appliance):
    assert rvc_appliance.is_feature_supported(MODE) is True


def test_is_feature_supported_false(rvc_appliance):
    assert rvc_appliance.is_feature_supported("invalid_cap") is False


def test_get_supported_modes(rvc_appliance):
    assert sorted(rvc_appliance.get_supported_modes()) == [1, 2, 3]


def test_is_docked(rvc_appliance):
    assert rvc_appliance.is_docked() is False


def test_is_paused(rvc_appliance):
    assert rvc_appliance.is_paused() is False


def test_get_current_readable_mode(rvc_appliance):
    assert rvc_appliance.get_current_mode() == 2


def test_get_current_state(rvc_appliance):
    assert rvc_appliance.get_current_state() == 10


def test_get_battery_percentage(rvc_appliance):
    assert rvc_appliance.get_battery_percentage() == 100.0


def test_get_start_command(rvc_appliance):
    cmd = rvc_appliance.get_start_command()
    assert cmd == {"CleaningCommand": "play"}


def test_get_resume_command(rvc_appliance):
    cmd = rvc_appliance.get_resume_command()
    assert cmd == {"CleaningCommand": "play"}


def test_get_stop_command(rvc_appliance):
    cmd = rvc_appliance.get_stop_command()
    assert cmd == {"CleaningCommand": "stop"}


def test_get_pause_command(rvc_appliance):
    cmd = rvc_appliance.get_pause_command()
    assert cmd == {"CleaningCommand": "pause"}


def test_get_dock_command(rvc_appliance):
    cmd = rvc_appliance.get_dock_command()
    assert cmd == {"CleaningCommand": "home"}


def test_get_set_mode_command(rvc_appliance):
    cmd = rvc_appliance.get_set_mode_command(3)
    assert cmd == {"powerMode": 3}


def test_start_zone_cleaning_command_valid(rvc_appliance):
    cmd = rvc_appliance.get_start_zone_cleaning_command("map1", ["kitchen"], 3)
    assert cmd == {
        "CustomPlay": {
            "persistentMapId": "map1",
            "zones": [
                {"zoneId": "kitchen", "powerMode": 3}]
        }
    }


def test_start_zone_cleaning_command_invalid(rvc_appliance):
    # Invalid cases: no zones or no map_id
    assert rvc_appliance.get_start_zone_cleaning_command("", ["z1"]) == {}
    assert rvc_appliance.get_start_zone_cleaning_command("map1", []) == {}


def test_gordias_start_room_cleaning_command(rvc_appliance):
    cmd = rvc_appliance.get_gordias_start_room_cleaning_command(
        map_id=1748953648,
        room_ids=[10, 11],
        sweep_mode=0,
        vacuum_mode="standard",
        water_pump_rate="off",
        number_of_repetitions=1
    )
    assert cmd == {
        "mapCommand": "selectRoomsClean",
        "mapId": 1748953648,
        "type": 1,
        "roomInfo": [
            {
                "roomId": 10,
                "sweepMode": 0,
                "vacuumMode": "standard",
                "waterPumpRate": "off",
                "numberOfCleaningRepetitions": 1
            },
            {
                "roomId": 11,
                "sweepMode": 0,
                "vacuumMode": "standard",
                "waterPumpRate": "off",
                "numberOfCleaningRepetitions": 1
            }
        ]
    }


def test_cybele_start_room_cleaning_command_global_settings_cleaning(rvc_appliance):
    cmd = rvc_appliance.get_cybele_start_room_cleaning_command(
        map_id=1748953648,
        room_ids_names=[(1, "bedroom"), (2, "kitchen")],
        global_settings_cleaning=False,
        cleaning_type="vacuum",
        vacuum_mode="standard",
        water_pump_rate="off",
        number_of_repetitions=1
    )
    assert cmd == {
        "mapCommand": "selectRoomsClean",
        "mapId": 1748953648,
        "type": 1,
        "roomInfo": [
            {
                "roomId": 1,
                "roomName": "bedroom",
                "cleaningType": "vacuum",
                "vacuumMode": "standard",
                "waterPumpRate": "off",
                "numberOfCleaningRepetitions": 1,
                "roomSequence": 0
            },
            {
                "roomId": 2,
                "roomName": "kitchen",
                "cleaningType": "vacuum",
                "vacuumMode": "standard",
                "waterPumpRate": "off",
                "numberOfCleaningRepetitions": 1,
                "roomSequence": 1
            }
        ]
    }


def test_cybele_start_room_cleaning_command_standard_settings_cleaning(rvc_appliance):
    cmd = rvc_appliance.get_cybele_start_room_cleaning_command(
        map_id=1748953648,
        room_ids_names=[(1, "bedroom"), (2, "kitchen")]
    )
    assert cmd == {
        "mapCommand": "selectRoomsClean",
        "mapId": 1748953648,
        "type": 0,
        "roomInfo": [
            {
                "roomId": 1,
            },
            {
                "roomId": 2,
            }
        ]
    }
