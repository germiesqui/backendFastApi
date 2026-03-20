from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.schemas.player import PlayerCreate, PlayerGoldUpdate, PlayerRead
from app.crud.player import create_player, get_players, get_player_by_name, get_player_by_id, update_player_gold


player_router = APIRouter()


@player_router.post("/", response_model=PlayerRead)
async def register_player(player_data: PlayerCreate, db: AsyncSession = Depends(get_db)):
    #TODO: comprobar si el nombre ya existe
    new_player = await create_player(db=db, player_data=player_data)
    return new_player

@player_router.get("/", response_model=list[PlayerRead])
async def read_all_players(db: AsyncSession = Depends(get_db)):
    all_players = await get_players(db=db)
    return all_players

@player_router.get("/id/{id}", response_model=PlayerRead)
async def read_player_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    player = await get_player_by_id(db=db, player_id=id)
    if player == None:
        raise HTTPException(status_code=404, detail="Player not found by that id")
    return player

@player_router.get("/name/{username}", response_model=PlayerRead)
async def read_player_by_name(username: str, db: AsyncSession = Depends(get_db)):
    player = await get_player_by_name(db=db, player_username=username)
    if player == None:
        raise HTTPException(status_code=404, detail="Player not found by that username")
    return player

@player_router.patch("/gold", response_model=PlayerRead)
async def read_player_by_name(player_data: PlayerGoldUpdate, db: AsyncSession = Depends(get_db)):
    player = await update_player_gold(db=db, player_data=player_data)
    return player