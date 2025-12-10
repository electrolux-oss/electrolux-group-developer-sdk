from typing import Any

from pydantic import BaseModel


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
