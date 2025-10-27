from datetime import datetime
from pydantic import BaseModel


class Appliance(BaseModel):
    applianceId: str
    applianceName: str
    applianceType: str
    created: datetime
