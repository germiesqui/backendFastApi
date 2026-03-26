import logging

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import invalidate_player_cache
from app.schemas.player import PlayerCreate, PlayerGoldUpdate
from app.models.base import Inventory, Player
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID

logger = logging.getLogger(__name__)

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

async def update_player_gold(db: AsyncSession, player_data: PlayerGoldUpdate):
    result = await db.execute(
        select(Player)
        .where(Player.id == player_data.id)
        .options(selectinload(Player.inventory_entries).selectinload(Inventory.item))
    )
    player = result.scalar_one_or_none()
    if not player:
        logger.warning(f"Player no encontrado | Player: {player_data.id} | Motivo: Ese id no existe")
        raise HTTPException(status_code=404, detail="El jugador no existe")
    
    updated_gold = player.gold + player_data.gold

    if updated_gold < 0:
        logger.warning(f"Update de oro invalido | Player: {player_data.id} | Oro Actual: {player.gold} | Oro a restar: {player_data.gold} | Motivo: El oro no puede ser negativo")
        raise HTTPException(status_code=400, detail="Un jugador no puede tener oro negativo.")
    
    player.gold = updated_gold

    await db.commit()
    await db.refresh(player)

    await invalidate_player_cache(player.id, player.username)
    
    return player