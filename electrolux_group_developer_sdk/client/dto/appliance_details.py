from typing import Any

from pydantic import BaseModel


class ApplianceInfo(BaseModel):
    serialNumber: str
    pnc: str
    brand: str
    deviceType: str
    model: str
    variant: str
    colour: str


class ApplianceDetails(BaseModel):
    applianceInfo: ApplianceInfo
    capabilities: dict[str, Any]
