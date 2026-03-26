from fastapi import FastAPI

from app.api.players import player_router
from app.api.items import item_router
from app.api.inventories import inventory_router
from app.core.logger import setup_logging
from app.core.redis import lifespan
from app.middleware.log_middleware import LogProcessTimeMiddleware

setup_logging()

app = FastAPI(title="Aetheria API", lifespan=lifespan)

app.include_router(player_router, prefix="/players", tags=["Players"])
app.include_router(item_router, prefix="/items", tags=["Items"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])

app.add_middleware(LogProcessTimeMiddleware)


@app.get("/")
async def root():
    return {"message": "Bienvenido a Aetheria"}
