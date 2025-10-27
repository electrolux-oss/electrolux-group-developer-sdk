from typing import Optional

from pydantic import BaseModel

from ...client.dto.appliance import Appliance
from ...client.dto.appliance_details import ApplianceDetails
from ...client.dto.appliance_state import ApplianceState


class ApplianceData(BaseModel):
    """Base appliance data class containing appliance details and state."""

    appliance: Appliance
    details: Optional[ApplianceDetails] = None
    state: Optional[ApplianceState] = None

    def update_state(self, state: ApplianceState) -> None:
        self.state = state
