from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.schemas.inventory import InventoryCreate
from app.models.base import Inventory
from sqlalchemy import select

async def add_item_to_inventory(db: AsyncSession, inventory_data: InventoryCreate):
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