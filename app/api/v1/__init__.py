from fastapi import APIRouter

from .users.router import router as users_router
from .tickets.router import router as tickets_router
from .subscription.router import router as subscription_router
from .exchanges.router import router as exchanges_router

router = APIRouter()

router.include_router(users_router, tags=["Users"])
router.include_router(tickets_router, tags=["Tickets"])
router.include_router(subscription_router, tags=["Subscription"])
router.include_router(exchanges_router, tags=["Exchanges"])
