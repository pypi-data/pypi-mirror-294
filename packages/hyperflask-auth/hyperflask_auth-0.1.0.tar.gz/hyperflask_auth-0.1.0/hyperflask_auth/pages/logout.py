from hyperflask import redirect, url_for, current_app
from hyperflask_auth.flow import logout


def get():
    logout()
    return redirect(current_app.extensions['auth'].logout_redirect_url)
