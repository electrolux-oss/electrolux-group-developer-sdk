from typing import Optional

from pydantic import BaseModel, Field


class Room(BaseModel):
    id: str
    name: str

class MemoryMap(BaseModel):
    id: str
    name: Optional[str] = None
    currentMap: bool
    rooms: Optional[list[Room]] = Field(default_factory=list)
