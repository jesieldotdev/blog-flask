# utils.py
from functools import wraps
from flask import redirect, url_for, flash, session
from models.__init_ import AuthUser  # Importe o modelo conforme sua estrutura de projeto

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthUser.check_if_user_admin(session.get("email")):
            flash("Você não está autorizado.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function