from typing import Any

from pydantic import BaseModel

from ..constants import TYPE, TYPE_STRING, VALUES


class ApplianceConfig(BaseModel):
    """Base appliance config class."""

    mapping: dict[str, Any]
    capabilities: dict[str, Any]

    def _get_state(self, state_key: str, reported_appliance_state: dict[str, Any]) -> Any:
        """Return the state given a specific key."""
        return reported_appliance_state.get(key) if (key := self.get_property(state_key)) else None

    def is_capability_supported(self, feature: str | list[str]):
        """Return True if the appliance supports this capability or any capability in a list."""
        if isinstance(feature, str):
            key = self.get_property(feature)
            return key is not None and key in self.capabilities
        elif isinstance(feature, list):
            for f in feature:
                key = self.get_property(f)
                if key is not None and key in self.capabilities:
                    return True
            return False
        return False

    def get_property(self, key: str) -> str:
        """Return the appliance type specific key."""
        return self.mapping.get(key)
    
    def get_feature_state_string_options(self, feature: str) -> list[str]:
        """Get the possible string values the property of a feature can be.
        
        This method is only usable for string type features."""
        capability = self.capabilities.get(self.get_property(feature))

        return self._get_capability_state_string_options(capability)
    
    def _get_capability_state_string_options(self, capability: dict[str, Any] | None) -> list[str]:
        """Get the possible string values the property of a feature can be. 

        This method is only usable for string type features."""
        if capability == None:
            return []

        if capability.get(TYPE) == TYPE_STRING:
            values = capability.get(VALUES, {})
            return [setting for setting in values]
        
        return []

