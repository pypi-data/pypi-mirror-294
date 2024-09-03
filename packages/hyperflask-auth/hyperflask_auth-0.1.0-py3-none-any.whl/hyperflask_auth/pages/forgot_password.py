from hyperflask import page, current_app, flash
from hyperflask_auth import UserModel
from hyperflask_auth.flow import send_reset_password_email


form = page.form()


def post():
    if form.validate():
        user = UserModel.find_one_or_404(email=form.email.data)
        send_reset_password_email(user)
        flash_msg = current_app.extensions['auth'].forgot_password_flash_message
        if flash_msg:
            flash(flash_msg)
