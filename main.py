import uvicorn

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from contextlib import asynccontextmanager

from src.api.v1.users.dao import create_admin
from src.api.v1.exchanges.dao import init_exchanges
from src.api.v1.tickets.dao import init_debug_tickets

from src.datebase import Base, engine
from src.api.v1 import api_router as router_v1, auth_router as auth_router
from src.admin.admin import admin
from src.config import get_secret_key

SECRET_KEY = get_secret_key()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_exchanges()
    await init_debug_tickets()
    await create_admin()
    yield


app = FastAPI(lifespan=lifespan)

admin.mount_to(app)

app.include_router(router_v1, prefix="/api/v1")
app.include_router(auth_router, prefix="/auth")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@app.get('/', tags=['Main'])
async def index():
    return {"status": "success", 'message': 'Hello, world!'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
