from typing import Dict, Any

from starlette.requests import Request

from app.api.v1.users.models import User
from app.api.v1.tickets.models import Ticket
from app.api.v1.subscription.models import Subscription
from app.api.v1.exchanges.models import Exchange

from app.api.v1.users.auth import get_password_hash
from app.datebase import engine

from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.views import Link

admin = Admin(engine, title="Collbit admin", logo_url="https://emojigraph.org/media/144/apple/gear_2699-fe0f.png",
              login_logo_url="https://emojigraph.org/media/144/apple/gear_2699-fe0f.png", base_url="/admin",
              route_name="admin",
              )


class UserView(ModelView):
    exclude_fields_from_list = [User.password]
    exclude_fields_from_create = [User.subscription, User.date_joined, User.last_login]
    exclude_fields_from_edit = [User.password]

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        extended_data = data.copy()
        extended_data["password"] = get_password_hash(extended_data['password'])
        return await super().create(request, extended_data)


class TicketView(ModelView):
    exclude_fields_from_list = [Ticket.available, Ticket.min_limit, Ticket.max_limit, Ticket.time_create,
                                Ticket.pay_methods]
    exclude_fields_from_create = [Ticket.time_create]
    exclude_fields_from_edit = [Ticket.time_create]


class SubscriptionView(ModelView):
    fields = [Subscription.id, Subscription.user, Subscription.subscription_type, Subscription.start_date,
              Subscription.end_date]

    exclude_fields_from_edit = [Subscription.start_date]
    exclude_fields_from_create = [Subscription.start_date]


class ExchangeView(ModelView):
    fields = [Exchange.id, Exchange.name]


admin.add_view(UserView(User))
admin.add_view(TicketView(Ticket))
admin.add_view(SubscriptionView(Subscription))
admin.add_view(ExchangeView(Exchange))
# admin.add_view(Link(label="Users from API", url="/api/v1/users"))
