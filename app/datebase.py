import os

from datetime import datetime
from typing import Annotated

from dotenv import load_dotenv

from sqlalchemy import func
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()
Base = declarative_base()
engine = create_async_engine(os.getenv('DATABASE_URL'))

async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
date_joined = Annotated[datetime, mapped_column(server_default=func.now())]
last_login = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]

