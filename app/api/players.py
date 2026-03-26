from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import logging


from app.database import get_db
from app.core.redis import cache_response, cache_player_by_id_key,cache_player_by_username_key
from app.schemas.player import PlayerCreate, PlayerGoldUpdate, PlayerRead
from app.crud.player import create_player, get_players, get_player_by_name, get_player_by_id, update_player_gold


player_router = APIRouter()
logger = logging.getLogger(__name__)

@player_router.post("/", response_model=PlayerRead)
async def register_player(player_data: PlayerCreate, db: AsyncSession = Depends(get_db)):
    existing_player: PlayerRead = await get_player_by_name(db=db, player_username=player_data.username)
    if existing_player:
        logger.warning(f"Username ya en uso | Username: {player_data.username} | Player: {existing_player.id} | Motivo: Ese username ya esta registrado por otro player")
        raise HTTPException(status_code=400, detail="Username already taken")
        
    new_player = await create_player(db=db, player_data=player_data)
    logger.info(f"Nuevo Player creado | Id: {new_player.id} | Username: {new_player.username}")
    return new_player


@player_router.get("/", response_model=list[PlayerRead])
async def read_all_players(db: AsyncSession = Depends(get_db)):
    all_players = await get_players(db=db)
    return all_players

@player_router.get("/id/{id}", response_model=PlayerRead)
@cache_response(cache_player_by_id_key, ttl=300)
async def read_player_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    player = await get_player_by_id(db=db, player_id=id)
    if player == None:
        logger.warning(f"Player no encontrado | Player: {id} | Motivo: Ese id no existe")
        raise HTTPException(status_code=404, detail="Player not found by that id")
    return player

@player_router.get("/name/{username}", response_model=PlayerRead)
@cache_response(cache_player_by_username_key, ttl=300)
async def read_player_by_name(username: str, db: AsyncSession = Depends(get_db)):
    player = await get_player_by_name(db=db, player_username=username)
    if player == None:
        logger.warning(f"Player no encontrado | Player: {username} | Motivo: Ese username no existe")
        raise HTTPException(status_code=404, detail="Player not found by that username")
    return player

@player_router.patch("/gold", response_model=PlayerRead)
async def patch_player_gold(player_data: PlayerGoldUpdate, db: AsyncSession = Depends(get_db)):
    player = await update_player_gold(db=db, player_data=player_data)
    return player