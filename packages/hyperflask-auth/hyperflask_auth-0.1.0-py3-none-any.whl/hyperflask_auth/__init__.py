from flask_login import current_user, LoginManager, login_required
from flask_file_routes import DEFAULT_HELPERS, decorator_as_page_helper, ModuleView
from sqlorm.sql_template import SQLTemplate
from jinja2 import FileSystemLoader
from hyperflask import lazy_gettext
from .model import UserMixin, UserModel, UserRelatedMixin, MissingUserModelError
from .blueprint import auth_blueprint
from .jinja_ext import LoginRequiredExtension, AnonymousOnlyExtension
from .flow import signup, login, logout, validate_password, send_reset_password_email, reset_password
from .signals import *
from dataclasses import dataclass
import typing as t
import os


@dataclass
class AuthState:
    signup_default_redirect_url: str
    reset_password_redirect_url: str
    login_redirect_url: str
    logout_redirect_url: str
    token_max_age: int
    allowed_methods: t.Sequence[str]
    forgot_password_flash_message: t.Optional[str]
    signup_email_template: t.Optional[str]
    reset_password_email_template: t.Optional[str]


class Auth:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app, register_blueprint=True):
        app.extensions['auth'] = AuthState(
            signup_default_redirect_url=app.config.get('AUTH_SIGNUP_DEFAULT_REDIRECT_URL', '/'),
            signup_email_template=app.config.get('AUTH_SIGNUP_EMAIL_TEMPLATE'),
            login_redirect_url=app.config.get('AUTH_LOGIN_REDIRECT_URL', '/'),
            forgot_password_flash_message=app.config.get('AUTH_FORGOT_PASSWORD_FLASH_MESSAGE', lazy_gettext("An email has been sent with instructions on how to reset your password")),
            reset_password_email_template=app.config.get('AUTH_RESET_PASSWORD_EMAIL_TEMPLATE'),
            reset_password_redirect_url=app.config.get('AUTH_RESET_PASSWORD_REDIRECT_URL', '/'),
            logout_redirect_url=app.config.get('AUTH_LOGOUT_REDIRECT_URL', '/'),
            token_max_age=app.config.get('AUTH_TOKEN_MAX_AGE', 3600),
            allowed_methods=app.config.get('AUTH_ALLOWED_METHODS', ['connect']),
        )

        manager = LoginManager(app)
        manager.login_view = 'auth.connect'

        @manager.user_loader
        def load_user(user_id):
            try:
                return UserModel.get(user_id)
            except MissingUserModelError:
                return

        DEFAULT_HELPERS.update(login_required=decorator_as_page_helper(login_required))
        ModuleView.module_globals.update(current_user=current_user)
        SQLTemplate.eval_globals.update(current_user=current_user)
        app.jinja_env.globals.update(current_user=current_user)
        app.jinja_env.add_extension(LoginRequiredExtension)
        app.jinja_env.add_extension(AnonymousOnlyExtension)
        app.extensions['mail_templates'].loaders.append(FileSystemLoader(os.path.join(os.path.dirname(__file__), 'emails')))
        app.assets.state.tailwind_suggested_content.append(os.path.join(os.path.dirname(__file__), "templates") + "/**/*.html")
        if register_blueprint:
            app.register_blueprint(auth_blueprint)
