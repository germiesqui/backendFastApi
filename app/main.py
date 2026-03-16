from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.item import ItemCreate, ItemRead
from app.schemas.player import PlayerCreate, PlayerRead
from app.crud.item import create_item
from app.crud.player import create_player

app = FastAPI(title="Aetheria API")

@app.post("/players/", response_model=PlayerRead)
async def register_player(player_data: PlayerCreate, db: AsyncSession = Depends(get_db)):
    #TODO: comprobar si el nombre ya existe
    new_player = await create_player(db=db, player_data=player_data)
    return new_player

@app.post("/items/", response_model=ItemRead)
async def register_item(item_data: ItemCreate, db: AsyncSession = Depends(get_db)):
    #TODO: comprobar si el nombre ya existe
    new_item = await create_item(db=db, item_data=item_data)
    return new_item