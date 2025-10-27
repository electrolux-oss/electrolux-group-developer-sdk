from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class Vertices(BaseModel):
    x: float
    y: float


class Zone(BaseModel):
    name: str
    id: str
    zoneType: str
    roomCategory: int
    powerMode: int
    vertices: list[Vertices] = Field(default_factory=list)

class InteractiveMap(BaseModel):
    zones: Optional[list[Zone]] = Field(default_factory=list)
    name: Optional[str] = None
    id: str
    rotation: float
    timestamp: datetime