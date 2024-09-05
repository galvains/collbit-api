from fastapi import APIRouter, HTTPException

from app.api.v1.subscription.schemas import *
from app.api.v1.subscription.dao import *

router = APIRouter()


@router.get("/subscriptions", summary="Get all subscriptions")
async def get_all_subscriptions():
    subscriptions = await db_get_all_subscriptions()
    if subscriptions:
        return {"status": "success", 'subscriptions': subscriptions}
    else:
        raise HTTPException(status_code=404, detail='Subscriptions not found')


@router.get("/subscription/{subscription_id}", summary="Get subscription")
async def get_all_subscriptions(subscription_id: int):
    subscription = await db_get_subscription(subscription_id)
    if subscription:
        return {"status": "success", 'subscription': subscription}
    else:
        raise HTTPException(status_code=404, detail='Subscription not found')


@router.post("/subscription", summary="Set new subscription")
async def create_subscription(subscription: SubscriptionCreateFilter):
    new_subscription = await db_add_new_subscription(**subscription.__dict__)
    if new_subscription:
        return {"status": "success", 'subscription': new_subscription}
    else:
        raise HTTPException(status_code=404, detail='Error added subscription')


@router.delete('/subscription/{subscription_id}', summary="Delete a subscription")
async def delete_subscription(subscription_id: int):
    delete = await db_del_subscription(subscription_id)
    if delete:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting subscription")


@router.put('/subscription', summary="Update a subscription")
async def update_subscription(subscription_update_filter: SubscriptionUpdateFilter,
                              new_data: SubscriptionNewDataFilter):
    updater_subscription = await db_upd_subscription(subscription_update_filter, new_data)
    if updater_subscription:
        return {"status": "success", 'subscription': updater_subscription}
    else:
        raise HTTPException(status_code=404, detail='Subscription not found')
