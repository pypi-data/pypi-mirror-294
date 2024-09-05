from hyperflask import page, request, redirect, url_for, current_app, abort
from hyperflask.utils.request import is_safe_redirect_url
from hyperflask_auth.flow import signup
from hyperflask_auth.captcha import validate_captcha_when_configured


if "signup" not in current_app.extensions['auth'].allowed_methods:
    if "connect" in current_app.extensions['auth'].allowed_methods:
        page.respond(redirect(url_for(".connect", next=request.args.get("next"))))
    abort(404)


form = page.form()


@validate_captcha_when_configured
def post():
    if form.validate():
        try:
            signup(form.data)
            next = request.args.get("next")
            return redirect(next if next and is_safe_redirect_url(next) else current_app.extensions['auth'].signup_default_redirect_url)
        except Exception as e:
            pass
