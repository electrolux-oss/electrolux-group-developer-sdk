from typing import Any

from pydantic import BaseModel


class ApplianceState(BaseModel):
    applianceId: str
    connectionState: str
    status: str
    properties: dict[str, Any]
