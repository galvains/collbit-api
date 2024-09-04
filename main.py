from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.exchanges.dao import init_exchanges
from app.api.v1.tickets.dao import init_debug_tickets
from app.datebase import Base, engine
from app.api.v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_exchanges()
    await init_debug_tickets()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix="/api/v1")


@app.get('/', tags=['Main'])
async def index():
    return {"status": "success", 'message': 'Hello, world!'}
