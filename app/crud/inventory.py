from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.schemas.inventory import InventoryCreate, InventoryDrop
from app.models.base import Inventory, Item, Player
from sqlalchemy import select

async def add_item_to_inventory(db: AsyncSession, inventory_data: InventoryCreate):
    await __player_check()
    await __item_check()

    query = select(Inventory).where(
        Inventory.item_id == inventory_data.item_id,
        Inventory.player_id == inventory_data.player_id
    ).options(selectinload(Inventory.item))
    result = await db.execute(query)
    inventory_entry = result.scalar_one_or_none()

    if inventory_entry:
        inventory_entry.quantity += inventory_data.quantity
    else:
        inventory_entry = Inventory(
            player_id=inventory_data.player_id,
            item_id=inventory_data.item_id,
            quantity=inventory_data.quantity
        )
        db.add(inventory_entry)
        
    await db.commit()
    await db.refresh(inventory_entry)

    return inventory_entry

async def drop_item_from_inventory(db: AsyncSession, inventory_data: InventoryDrop):
    await __player_check()
    await __item_check()

    query = select(Inventory).where(
        Inventory.item_id == inventory_data.item_id,
        Inventory.player_id == inventory_data.player_id
    ).options(selectinload(Inventory.item))
    result = await db.execute(query)
    inventory_entry = result.scalar_one_or_none()

    if not inventory_entry:
        raise HTTPException(status_code=404, detail="El jugador no tiene ese item.")

    if inventory_data.quantity > inventory_entry.quantity:
        raise HTTPException(status_code=400, detail="El jugador no tiene tantas unidades de ese item.")
    
    if inventory_data.quantity == inventory_entry.quantity:
        await db.delete(inventory_entry)
        inventory_entry = None

    await db.commit()

    if inventory_entry:
        await db.refresh(inventory_entry)
        
    return inventory_entry

    

async def __player_check(db: AsyncSession, player_id: UUID):
    player_check = await db.get(Player, player_id)
    if not player_check:
        raise HTTPException(status_code=404, detail="El jugador no existe.")

async def __item_check(db: AsyncSession, item_id: UUID):
    item_check = await db.get(Item, item_id)
    if not item_check:
        raise HTTPException(status_code=404, detail="El ítem no existe.")