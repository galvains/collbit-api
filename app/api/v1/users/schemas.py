from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class UserRoles(Enum):
    user = 'user'
    admin = 'admin'
    staff = 'staff'


class UserRegistrationFilter(BaseModel):
    telegram_id: int
    username: str
    password: str | None
    role: UserRoles


class UserUpdateFilter(BaseModel):
    user_id: int


class UserNewDataFilter(BaseModel):
    username: str
    password: str
    role: UserRoles
    is_subscriber: bool
    last_login: datetime
