from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.item import ItemCreate
from app.models.base import Item
from sqlalchemy.future import select

async def create_item(db: AsyncSession, item_data: ItemCreate):
    new_item = Item(name=item_data.name, description=item_data.description)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

async def get_items(db: AsyncSession):
    query = select(Item)
    result = await db.execute(query)
    
    return result.scalars().all()

async def get_item_by_name(db: AsyncSession, item_name: str):
    result = await db.execute(
        select(Item)
        .where(Item.name == item_name)
    )
    
    return result.scalar_one_or_none()

async def get_item_by_id(db: AsyncSession, item_id: int):
    result = await db.execute(
        select(Item)
        .where(Item.id == item_id)
    )
    
    return result.scalar_one_or_none()