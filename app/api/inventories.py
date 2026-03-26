import logging

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.inventory import InventoryCreate, InventoryDrop, InventoryRead
from app.crud.inventory import add_item_to_inventory, drop_item_from_inventory

inventory_router = APIRouter()
logger = logging.getLogger(__name__)

@inventory_router.post("/add", response_model=InventoryRead)
async def add_item_to_player(inventory_data: InventoryCreate, db: AsyncSession = Depends(get_db)):
    inventory_entry = await add_item_to_inventory(db=db, inventory_data=inventory_data)
    logger.info(f"Entrada de inventario creada | Player: {inventory_entry.player_id} | Item: {inventory_entry.item_id} | Quantity: {inventory_entry.quantity}")
    return inventory_entry

@inventory_router.delete("/drop")
async def drop_item(inventory_data: InventoryDrop, db: AsyncSession = Depends(get_db)):
    inventory_entry = await drop_item_from_inventory(db=db, inventory_data=inventory_data)

    if inventory_entry is None:
        logger.info(f"Entrada de inventario eliminada | Player: {inventory_data.player_id} | Item: {inventory_data.item_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        logger.info(f"Entrada de inventario actualizada | Player: {inventory_entry.player_id} | Item: {inventory_entry.item_id} | New Quantity: {inventory_entry.quantity}")
    
    return inventory_entry