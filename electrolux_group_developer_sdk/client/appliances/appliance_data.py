from abc import abstractmethod
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
    
    @abstractmethod
    def is_feature_supported(self, feature: str | list[str]) -> bool:
        """Check if a feature is supported for the appliance."""
    
    @abstractmethod
    def get_feature_state_string_options(self, feature: str) -> list[str]:
        """Get the possible string values the property of a feature can be.
        
        This method is only usable for string type features."""
