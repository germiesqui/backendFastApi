from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.player import PlayerCreate
from app.models.base import Player
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

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