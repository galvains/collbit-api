from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class UserRoles(Enum):
    user = 'user'
    staff = 'staff'
    admin = 'admin'


class UserRegistrationFilter(BaseModel):
    telegram_id: int
    username: str
    password: str | None
    # role: UserRoles


class UserUpdateFilter(BaseModel):
    user_id: int


class UserNewDataFilter(BaseModel):
    username: str
    password: str
    role: UserRoles
    last_login: datetime | None
    subscription_id: int | None


class UserAuthFilter(BaseModel):
    telegram_id: int
    password: str
