from fastapi import FastAPI

from app.api.players import player_router
from app.api.items import item_router
from app.api.inventories import inventory_router


app = FastAPI(title="Aetheria API")

app.include_router(player_router, prefix="/players", tags=["Players"])
app.include_router(item_router, prefix="/items", tags=["Items"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])


@app.get("/")
async def root():
    return {"message": "Bienvenido a las tierras de Aetheria"}
