from .appliances.ac_appliance import ACAppliance
from .appliances.ap_appliance import APAppliance
from .appliances.cr_appliance import CRAppliance
from .appliances.dam_ac_appliance import DAMACAppliance
from .appliances.dh_appliance import DHAppliance
from .appliances.dw_appliance import DWAppliance
from .appliances.hb_appliance import HBAppliance
from .appliances.hd_appliance import HDAppliance
from .appliances.ov_appliance import OVAppliance
from .appliances.rvc_appliance import RVCAppliance
from .appliances.so_appliance import SOAppliance
from .appliances.td_appliance import TDAppliance
from .appliances.wd_appliance import WDAppliance
from .appliances.wm_appliance import WMAppliance
from .dto.appliance import Appliance
from .dto.appliance_details import ApplianceDetails
from .dto.appliance_state import ApplianceState
from ..client.appliances.appliance_data import ApplianceData
from ..constants import AC, CA, AZUL, BOGONG, PANTHER, TELICA, MUJU, FUJI, PUREA9, VERBIER, WELLA5, WELLA7, DH, HUSKY, \
    PUREI9, GORDIAS, SERIES_700, OV, TD, WM, WD, DW, HB, HD, CR, SO, DAM_AC, CYBELE

APPLIANCE_TYPE_CLASS_MAP: dict[str, type[ApplianceData]] = {
    # Air Conditioner
    AC: ACAppliance,
    CA: ACAppliance,
    AZUL: ACAppliance,
    BOGONG: ACAppliance,
    PANTHER: ACAppliance,
    TELICA: ACAppliance,
    DAM_AC: DAMACAppliance,
    # Air Purifier
    MUJU: APAppliance,
    FUJI: APAppliance,
    PUREA9: APAppliance,
    VERBIER: APAppliance,
    WELLA5: APAppliance,
    WELLA7: APAppliance,
    # Dehumidifier
    DH: DHAppliance,
    HUSKY: DHAppliance,
    # RVC
    PUREI9: RVCAppliance,
    GORDIAS: RVCAppliance,
    CYBELE: RVCAppliance,
    SERIES_700: RVCAppliance,
    # Care
    TD: TDAppliance,
    WM: WMAppliance,
    WD: WDAppliance,
    DW: DWAppliance,
    # Taste
    OV: OVAppliance,
    HB: HBAppliance,
    HD: HDAppliance,
    CR: CRAppliance,
    SO: SOAppliance
}


def appliance_data_factory(
        appliance: Appliance,
        details: ApplianceDetails,
        state: ApplianceState,
) -> ApplianceData:
    """
    Return an instance of the appropriate ApplianceData subclass based on appliance type.

    If no subclass is defined for the appliance type, the base ApplianceData class is returned.
    """
    cls = APPLIANCE_TYPE_CLASS_MAP.get(appliance.applianceType, ApplianceData)
    return cls(appliance=appliance, details=details, state=state)
