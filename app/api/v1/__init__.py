from fastapi import APIRouter, Depends

from .users.router import router as users_router
from .users.auth import router as _router, is_default_user
from .tickets.router import router as tickets_router
from .subscription.router import router as subscription_router
from .exchanges.router import router as exchanges_router

api_router = APIRouter(dependencies=[Depends(is_default_user)])
auth_router = APIRouter()
api_router.include_router(users_router, tags=["Users"])
api_router.include_router(tickets_router, tags=["Tickets"])
api_router.include_router(subscription_router, tags=["Subscription"])
api_router.include_router(exchanges_router, tags=["Exchanges"])

auth_router.include_router(_router, tags=["Auth"])
