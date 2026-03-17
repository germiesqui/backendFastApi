from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.player import PlayerCreate
from app.models.base import Inventory, Player
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID

async def create_player(db: AsyncSession, player_data: PlayerCreate):
    new_player = Player(username=player_data.username)
    db.add(new_player)
    await db.commit()

    result = await db.execute(
        select(Player)
        .where(Player.username == player_data.username)
        .options(selectinload(Player.inventory_entries))
    )
    return result.scalar_one()

async def get_players(db: AsyncSession):
    query = select(Player).options(selectinload(Player.inventory_entries).selectinload(Inventory.item))
    result = await db.execute(query)
    
    return result.scalars().all()

async def get_player_by_name(db: AsyncSession, player_username: str):
    result = await db.execute(
        select(Player)
        .where(Player.username == player_username)
        .options(selectinload(Player.inventory_entries).selectinload(Inventory.item))
    )
    
    return result.scalar_one_or_none()

async def get_player_by_id(db: AsyncSession, player_id: UUID):
    result = await db.execute(
        select(Player)
        .where(Player.id == player_id)
        .options(selectinload(Player.inventory_entries).selectinload(Inventory.item))
    )
    
    return result.scalar_one_or_none()