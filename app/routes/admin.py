from flask import Blueprint, abort
from flask_login import login_required, current_user

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if not current_user.has_role("admin"):
        abort(403)

    return "Admin dashboard soon coming, be cool"