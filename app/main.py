from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


from app.database import get_db
from app.schemas.inventory import InventoryCreate, InventoryRead
from app.schemas.item import ItemCreate, ItemRead
from app.schemas.player import PlayerCreate, PlayerRead
from app.crud.item import create_item, get_items, get_item_by_id, get_item_by_name
from app.crud.player import create_player, get_players, get_player_by_name, get_player_by_id
from app.crud.inventory import add_item_to_inventory


app = FastAPI(title="Aetheria API")

#------ PLAYER --------#
@app.post("/players/", response_model=PlayerRead)
async def register_player(player_data: PlayerCreate, db: AsyncSession = Depends(get_db)):
    #TODO: comprobar si el nombre ya existe
    new_player = await create_player(db=db, player_data=player_data)
    return new_player

@app.get("/players/", response_model=list[PlayerRead])
async def read_all_players(db: AsyncSession = Depends(get_db)):
    all_players = await get_players(db=db)
    return all_players

@app.get("/players/id/{id}", response_model=PlayerRead)
async def read_player_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    player = await get_player_by_id(db=db, player_id=id)
    if player == None:
        raise HTTPException(status_code=404, detail="Player not found by that id")
    return player

@app.get("/players/name/{username}", response_model=PlayerRead)
async def read_player_by_name(username: str, db: AsyncSession = Depends(get_db)):
    player = await get_player_by_name(db=db, player_username=username)
    if player == None:
        raise HTTPException(status_code=404, detail="Player not found by that username")
    return player


#------ ITEM --------#

@app.post("/items/", response_model=ItemRead)
async def register_item(item_data: ItemCreate, db: AsyncSession = Depends(get_db)):
    #TODO: comprobar si el nombre ya existe
    new_item = await create_item(db=db, item_data=item_data)
    return new_item

@app.get("/items/", response_model=list[ItemRead])
async def read_all_items(db: AsyncSession = Depends(get_db)):
    all_items = await get_items(db=db)
    return all_items

@app.get("/items/id/{id}", response_model=ItemRead)
async def read_item_by_id(id: int, db: AsyncSession = Depends(get_db)):
    item = await get_item_by_id(db=db, item_id=id)
    if item == None:
        raise HTTPException(status_code=404, detail="Item not found by that id")
    return item

@app.get("/items/name/{name}", response_model=ItemRead)
async def read_item_by_name(name: str, db: AsyncSession = Depends(get_db)):
    item = await get_item_by_name(db=db, item_name=name)
    if item == None:
        raise HTTPException(status_code=404, detail="Item not found by that name")
    return item

#------ INVENTORY --------#
@app.post("/inventory/add", response_model=InventoryRead)
async def add_item_to_player(inventory_data: InventoryCreate, db: AsyncSession = Depends(get_db)):
    inventory_entry = await add_item_to_inventory(db=db, inventory_data=inventory_data)
    return inventory_entry