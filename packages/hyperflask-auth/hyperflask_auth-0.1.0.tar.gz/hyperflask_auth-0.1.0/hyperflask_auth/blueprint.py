from flask import Blueprint
from flask_file_routes import ModuleView


auth_blueprint = Blueprint("auth", __name__, template_folder="templates")

ModuleView("hyperflask_auth.pages.connect", "auth/connect.html").register(auth_blueprint, "/connect", methods=["GET", "POST"])
ModuleView("hyperflask_auth.pages.login", "auth/login.html").register(auth_blueprint, "/login", methods=["GET", "POST"])
ModuleView("hyperflask_auth.pages.login_link", "auth/login_link.html").register(auth_blueprint, "/login/link", methods=["GET", "POST"])
ModuleView("hyperflask_auth.pages.signup", "auth/signup.html").register(auth_blueprint, "/signup", methods=["GET", "POST"])
ModuleView("hyperflask_auth.pages.forgot_password", "auth/forgot_password.html").register(auth_blueprint, "/login/forgot", methods=["GET", "POST"])
ModuleView("hyperflask_auth.pages.reset_password", "auth/reset_password.html").register(auth_blueprint, "/login/reset", methods=["GET", "POST"])
ModuleView("hyperflask_auth.pages.logout", None).register(auth_blueprint, "/logout", methods=["GET"])
