from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import List
from .inventory import InventoryRead

class PlayerCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=16)

class PlayerRead(BaseModel):
    id: UUID
    username: str = Field(min_length=3, max_length=16)
    gold: int = Field(ge=0)
    inventory_entries: List["InventoryRead"] = []

    model_config = ConfigDict(from_attributes=True)