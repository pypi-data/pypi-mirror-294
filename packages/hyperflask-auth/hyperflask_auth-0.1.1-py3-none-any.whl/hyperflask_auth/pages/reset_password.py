from hyperflask import redirect, request, page, current_app
from hyperflask.utils.request import is_safe_redirect_url
from hyperflask_auth import UserModel
from hyperflask_auth.flow import reset_password
from hyperflask_auth.captcha import validate_captcha_when_configured


form = page.form()
user = UserModel.from_token_or_404(request.args["token"], max_age=current_app.extensions['auth'].token_max_age)


@validate_captcha_when_configured
def post():
    if form.validate():
        try:
            reset_password(user, form.password.data)
            next = request.args.get("next", current_app.extensions['auth'].reset_password_redirect_url)
            if next and is_safe_redirect_url(next):
                return redirect(next)
        except:
            pass
