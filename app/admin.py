from typing import Dict, Any

from app.api.v1.users.models import User
from app.api.v1.tickets.models import Ticket
from app.api.v1.subscription.models import Subscription
from app.api.v1.exchanges.models import Exchange

from app.api.v1.users.auth import get_password_hash
from app.datebase import engine
from app.config import admin as admin_data

from starlette_admin.contrib.sqla import Admin, ModelView

from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

users = {
    admin_data.username: {
        "name": admin_data.username,
        "avatar": None,
        "roles": ["read", "create", "edit", "delete", "action_make_published"],
    },
}


class UsernameAndPasswordProvider(AuthProvider):

    async def login(
            self,
            username: str,
            password: str,
            remember_me: bool,
            request: Request,
            response: Response,
    ) -> Response:
        if len(username) < 3:
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )

        if username in users and password == admin_data.password:
            request.session.update({"username": username})
            return response
        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) in users:
            request.state.user = users.get(request.session["username"])
            return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user
        custom_app_title = "Hello, " + user["name"] + "!"
        custom_logo_url = None

        # if user.get("company_logo_url", None):
        #     custom_logo_url = request.url_for("static", path=user["company_logo_url"])
        return AdminConfig(
            app_title=custom_app_title,
            logo_url=custom_logo_url,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user
        photo_url = None

        # if user["avatar"] is not None:
        #     photo_url = request.url_for("static", path=user["avatar"])
        return AdminUser(username=user["name"], photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response


admin = Admin(engine, title="Collbit admin", logo_url="https://emojigraph.org/media/144/apple/gear_2699-fe0f.png",
              login_logo_url="https://emojigraph.org/media/144/apple/gear_2699-fe0f.png", base_url="/admin",
              route_name="admin", auth_provider=UsernameAndPasswordProvider())


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
