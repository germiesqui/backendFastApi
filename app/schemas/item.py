from pydantic import BaseModel, Field, ConfigDict

class ItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=16)
    description: str = Field(default="", max_length=64)

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)