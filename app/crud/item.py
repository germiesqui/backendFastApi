from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.item import ItemCreate
from app.models.base import Item

async def create_item(db: AsyncSession, item_data: ItemCreate):
    new_item = Item(name=item_data.name, description=item_data.description)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item