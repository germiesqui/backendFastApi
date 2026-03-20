
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.item import ItemCreate, ItemRead
from app.crud.item import create_item, get_items, get_item_by_id, get_item_by_name

item_router = APIRouter()

@item_router.post("/", response_model=ItemRead)
async def register_item(item_data: ItemCreate, db: AsyncSession = Depends(get_db)):
    #TODO: comprobar si el nombre ya existe
    new_item = await create_item(db=db, item_data=item_data)
    return new_item

@item_router.get("/", response_model=list[ItemRead])
async def read_all_items(db: AsyncSession = Depends(get_db)):
    all_items = await get_items(db=db)
    return all_items

@item_router.get("/id/{id}", response_model=ItemRead)
async def read_item_by_id(id: int, db: AsyncSession = Depends(get_db)):
    item = await get_item_by_id(db=db, item_id=id)
    if item == None:
        raise HTTPException(status_code=404, detail="Item not found by that id")
    return item

@item_router.get("/name/{name}", response_model=ItemRead)
async def read_item_by_name(name: str, db: AsyncSession = Depends(get_db)):
    item = await get_item_by_name(db=db, item_name=name)
    if item == None:
        raise HTTPException(status_code=404, detail="Item not found by that name")
    return item
