import time
from typing import Optional

from fastapi import FastAPI

from models import Base, engine
from queries import init_exchanges, init_debug_tickets, db_get_all_tickets, db_get_filtered_ticket

app = FastAPI()
Base.metadata.create_all(engine)
init_exchanges()
init_debug_tickets()


@app.get('/')
def index():
    return {'message': 'Hello, world!'}


@app.get('/api/v1/tickets')
def get_all_tickets():
    return db_get_all_tickets()


@app.get('/api/v1/ticket')
def get_filtered_ticket(coin: Optional[str] = 'USDT', currency: Optional[str] = 'USD',
                        trade_type: Optional[str] = 'BUY'):
    total_data = db_get_filtered_ticket(coin.upper(), currency.upper(), trade_type.upper())
    return total_data
