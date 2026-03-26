
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.database import get_db
from app.schemas.item import ItemCreate, ItemRead
from app.crud.item import create_item, get_items, get_item_by_id, get_item_by_name

item_router = APIRouter()
logger = logging.getLogger(__name__)

@item_router.post("/", response_model=ItemRead)
async def register_item(item_data: ItemCreate, db: AsyncSession = Depends(get_db)):
    existing_item: ItemRead = await get_item_by_name(db=db, item_name=item_data.name)
    if existing_item:
        logger.warning(f"Nombre invalido | Name: {item_data.name} | Item: {existing_item.id} | Motivo: Ya existe un item con ese nombre")
        raise HTTPException(status_code=400, detail="Item with same name already exist")
    
    new_item = await create_item(db=db, item_data=item_data)
    logger.info(f"Nuevo Item creado | Id: {new_item.id} | Name: {new_item.name}")
    return new_item

@item_router.get("/", response_model=list[ItemRead])
async def read_all_items(db: AsyncSession = Depends(get_db)):
    all_items = await get_items(db=db)
    return all_items

@item_router.get("/id/{id}", response_model=ItemRead)
async def read_item_by_id(id: int, db: AsyncSession = Depends(get_db)):
    item = await get_item_by_id(db=db, item_id=id)
    if item == None:
        logger.warning(f"Item no encontrado | Item Id: {id} | Motivo: Ese id no existe")
        raise HTTPException(status_code=404, detail="Item not found by that id")
    return item

@item_router.get("/name/{name}", response_model=ItemRead)
async def read_item_by_name(name: str, db: AsyncSession = Depends(get_db)):
    item = await get_item_by_name(db=db, item_name=name)
    if item == None:
        logger.warning(f"Item no encontrado | Name: {name} | Motivo: Ese item no existe")
        raise HTTPException(status_code=404, detail="Item not found by that name")
    return item
