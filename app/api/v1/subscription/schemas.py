from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class TypesSubscription(Enum):
    lite = 'lite'
    medium = 'medium'
    hard = 'hard'


class SubscriptionCreateFilter(BaseModel):
    user_id: int
    subscription_type: TypesSubscription
    end_date: datetime


class SubscriptionUpdateFilter(BaseModel):
    subscription_id: int


class SubscriptionNewDataFilter(BaseModel):
    subscription_type: TypesSubscription
    start_date: datetime
    end_date: datetime
