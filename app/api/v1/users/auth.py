import os

from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Response, Request, Depends

from app.api.v1.users.schemas import UserRegistrationFilter, UserAuthFilter
from app.api.v1.users.models import User

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    return token


async def authenticate_user(telegram_id: int, password: str):
    from app.api.v1.users.dao import db_get_user_by_any_filter
    user = await db_get_user_by_any_filter(telegram_id=telegram_id)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


async def is_default_user(token: str = Depends(get_token)):
    from app.api.v1.users.dao import db_get_user_by_any_filter
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as ex:
        raise HTTPException(status_code=401, detail="Could not validate token")

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=401, detail="Token expired")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User's id not found")

    user = await db_get_user_by_any_filter(id=int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


async def is_staff_user(current_user: User = Depends(is_default_user)):
    if current_user.role in ['staff', 'admin']:
        return current_user
    raise HTTPException(status_code=401, detail="Not enough permissions")


async def is_admin_user(current_user: User = Depends(is_default_user)):
    if current_user.role == 'admin':
        return current_user
    raise HTTPException(status_code=403, detail="Not enough permissions")


@router.post("/register")
async def register_user(user_data: UserRegistrationFilter):
    from app.api.v1.users.dao import db_add_new_user

    new_user = await db_add_new_user(**user_data.model_dump())
    if new_user:
        return {"status": "success", 'user': new_user}
    else:
        raise HTTPException(status_code=409, detail='User already exists')


@router.post("/login")
async def auth_user(response: Response, user_data: UserAuthFilter):
    check = await authenticate_user(telegram_id=user_data.telegram_id, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access_token = create_access_token({'sub': str(check.id)})
    response.set_cookie(key='user_access_token', value=access_token, httponly=True)
    return {"access_token": access_token, 'refresh_token': None}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key='user_access_token')
    return {"status": "success", 'message': "User logged out"}


@router.get("/me")
async def get_me(user_data: User = Depends(is_default_user)):
    return user_data
