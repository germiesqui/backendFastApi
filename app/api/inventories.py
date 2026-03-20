from alembic.util import status
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.inventory import InventoryCreate, InventoryDrop, InventoryRead
from app.crud.inventory import add_item_to_inventory, drop_item_from_inventory

inventory_router = APIRouter()

@inventory_router.post("/add", response_model=InventoryRead)
async def add_item_to_player(inventory_data: InventoryCreate, db: AsyncSession = Depends(get_db)):
    inventory_entry = await add_item_to_inventory(db=db, inventory_data=inventory_data)
    return inventory_entry

@inventory_router.delete("/drop")
async def drop_item(inventory_data: InventoryDrop, db: AsyncSession = Depends(get_db)):
    inventory_entry = await drop_item_from_inventory(db=db, inventory_data=inventory_data)

    if inventory_entry is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return inventory_entry