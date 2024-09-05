from flask_login import login_user, logout_user
from hyperflask import send_mail, current_app, db
import random
import datetime
from . import signals
from .passlib import hash_password
from .model import UserModel


def signup(data=None, **kwargs):
    data = dict(data) if data else {}
    data.update(kwargs)

    if "password" in data:
        if not validate_password(data['password']):
            raise Exception()
        data['password'] = hash_password(data['password'])

    signals.user_before_signup.send(current_app, data=data)
    with db:
        user = UserModel.create(**data)
    signals.user_signed_up.send(current_app, user=user)
    login(user)
    email_template = current_app.extensions['auth'].signup_email_template
    if email_template:
        send_mail(email_template, user.email, user=user)
    return user


def login(user, password=None, remember=False, login_using=None):
    if password and not user.verify_password(password):
        raise Exception()
    login_user(user, remember=remember)
    with db:
        user.last_login_at = datetime.datetime.utcnow()
        user.last_login_using = login_using
        user.save()


def send_login_link(user):
    token = user.create_token()
    code = str(random.randrange(10000, 99999))
    send_mail("auth/login_link.mjml", user.email, token=token, code=code)
    return code


def logout():
    logout_user()


def validate_password(password):
    return True


def send_reset_password_email(user):
    token = user.create_token()
    send_mail("auth/forgot_password.mjml", user.email, token=token)
    return token


def reset_password(user, password):
    if not validate_password(password):
        raise Exception()

    with db:
        user.update_password(password)

    login(user)
    email_template = current_app.extensions['auth'].reset_password_email_template
    if email_template:
        send_mail(email_template, user.email, user=user)
