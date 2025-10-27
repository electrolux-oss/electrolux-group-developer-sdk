from typing import Dict, Any

from pydantic import BaseModel


class ApplianceState(BaseModel):
    applianceId: str
    connectionState: str
    status: str
    properties: Dict[str, Any]
