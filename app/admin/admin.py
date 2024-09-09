from app.api.v1.users.models import User
from app.api.v1.tickets.models import Ticket
from app.api.v1.subscription.models import Subscription
from app.api.v1.exchanges.models import Exchange

from app.admin.views import UserView, TicketView, SubscriptionView, ExchangeView
from app.admin.auth import UsernameAndPasswordProvider

from app.datebase import engine

from starlette_admin.contrib.sqla import Admin

admin = Admin(engine, title="Collbit admin", logo_url="https://emojigraph.org/media/144/apple/gear_2699-fe0f.png",
              login_logo_url="https://emojigraph.org/media/144/apple/gear_2699-fe0f.png", base_url="/admin",
              route_name="admin", auth_provider=UsernameAndPasswordProvider())

admin.add_view(UserView(User))
admin.add_view(TicketView(Ticket))
admin.add_view(SubscriptionView(Subscription))
admin.add_view(ExchangeView(Exchange))
