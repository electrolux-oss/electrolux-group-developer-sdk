from pydantic import BaseModel


class LivestreamAppliance(BaseModel):
    applianceId: str
    properties: list[str]


class LivestreamConfig(BaseModel):
    url: str
    appliances: list[LivestreamAppliance]