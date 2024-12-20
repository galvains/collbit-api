from datetime import datetime

from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError

from src.api.v1.subscription.models import Subscription
from src.api.v1.subscription.schemas import TypesSubscription
from src.api.v1.users.models import User
from src.datebase import async_session_factory


async def db_get_all_subscriptions():
    try:
        async with async_session_factory() as session:
            query = await session.execute(select(Subscription))
            all_subscriptions = query.scalars().all()

            return all_subscriptions
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_get_subscription_by_any_filter(**filter_by):
    try:
        async with async_session_factory() as session:
            query = await session.execute(select(Subscription).filter_by(**filter_by))
            subscription = query.scalars().first()

            return subscription
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_add_new_subscription(**filter_by):
    for key, value in filter_by.items():
        if isinstance(value, TypesSubscription):
            filter_by[key] = value.value
        if isinstance(value, datetime):
            filter_by[key] = value.replace(tzinfo=None)

    user_id = filter_by.pop('user_id')

    try:
        async with async_session_factory() as session:
            query = await session.execute(select(User).filter_by(id=user_id))
            user = query.scalars().one_or_none()
            if user is None:
                return False

            new_subscription = Subscription(**filter_by)
            session.add(new_subscription)

            await session.commit()
            user.subscription_id = new_subscription.id

            await session.commit()
            await session.refresh(new_subscription)

            return {'id': new_subscription.id,
                    'subscription_type': new_subscription.subscription_type,
                    'start_date': new_subscription.start_date,
                    'end_date': new_subscription.end_date,}

    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_del_subscription(subscription_id):
    try:
        async with async_session_factory() as session:
            deleted_count = await session.execute(delete(Subscription).filter_by(id=subscription_id))
            await session.commit()

            return deleted_count.rowcount > 0
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_upd_subscription(subscription_update_filter, new_data):
    subscription_id = subscription_update_filter.subscription_id

    try:
        async with async_session_factory() as session:
            query = await session.execute(select(Subscription).filter_by(id=subscription_id))
            check_subscription = query.scalars().one_or_none()

            if check_subscription:
                for key, value in new_data:
                    if isinstance(value, datetime):
                        value = value.replace(tzinfo=None)

                    await session.execute(
                        update(Subscription).where(Subscription.id == subscription_id).values({key: value}))

                await session.commit()
                await session.refresh(check_subscription)
                return {'id': check_subscription.id, 'subscription_type': check_subscription.subscription_type}
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()
