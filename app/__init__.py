from flask import Flask, request, render_template
from config import Config
from app.extensions import db, migrate, login_manager, csrf, limiter
from datetime import timezone
from zoneinfo import ZoneInfo
from app.forms.auth import PasswordResetVerificationForm
from app.routes.support import support_bp

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    # Initialise extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Timezone conversion to EAT(Kenyan time)
    nairobi_tz = ZoneInfo("Africa/Nairobi")

    @app.template_filter("kenya_time")
    def kenya_time(value, format="%d %b %Y, %I:%M %p"):
        if value is None:
            return ""

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        return value.astimezone(nairobi_tz).strftime(format)

    from app import models

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.citizen import citizen_bp
    from app.routes.requests import requests_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(citizen_bp)
    app.register_blueprint(requests_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(support_bp)

    @app.errorhandler(429)
    def handle_rate_limit(error):
        if request.endpoint == "auth.forgot_password":
            form = PasswordResetVerificationForm()

            return render_template(
                "auth/forgot_password.html",
                stage="verify",
                verification_form=form,
                reset_form=None,
                rate_limited=True,
            ), 429

        return "Too many attempts. Please try again later.", 429

    return app
