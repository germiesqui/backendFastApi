from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from .item import ItemRead

class InventoryCreate(BaseModel):
    player_id: UUID = Field(...)
    item_id: int = Field(...)
    quantity: int = Field(..., ge=1)

class InventoryRead(BaseModel):
    quantity: int
    item: ItemRead

    model_config = ConfigDict(from_attributes=True)
