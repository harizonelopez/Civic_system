from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
    make_response,
)
from flask_login import login_user, logout_user, current_user
from app.extensions import db, limiter
from app.models import User, Role
from app.forms.auth import (
    RegistrationForm,
    LoginForm,
    PasswordResetVerificationForm,
    PasswordResetForm,
)
from urllib.parse import urlsplit
from datetime import datetime, timedelta, timezone

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        next_page = request.args.get("next")
        if next_page:
            parsed_url = urlsplit(next_page)
            if (
                next_page.startswith("/")
                and not next_page.startswith("//")
                and not parsed_url.netloc
                and not parsed_url.scheme
            ):
                return redirect(next_page)
        return redirect(url_for("citizen.dashboard"))

    form = RegistrationForm()    
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
            return render_template("auth/register.html", form=form)

        # Check whether the National ID is already registered.
        if User.query.filter_by(national_id=form.national_id.data.strip()).first():
            flash("An account with this National ID already exists.", "danger")
            return render_template("auth/register.html", form=form)

        # Check whether the phone number is already registered.
        phone_number = form.phone_number.data.strip() if form.phone_number.data else None

        if phone_number and User.query.filter_by(phone_number=phone_number).first():
            flash("An account with this phone number already exists.", "danger")
            return render_template("auth/register.html", form=form)

        user = User(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            email=email,
            phone_number=form.phone_number.data.strip() if form.phone_number.data else None,
            gender=form.gender.data,
            national_id=form.national_id.data.strip(),
        )

        user.set_password(form.password.data)

        # Assign the citizen role to newly registered accounts.
        citizen_role = Role.query.filter_by(name="citizen").first()

        if not citizen_role:
            flash("Citizen registration currently unavailable. Contact the administrator.", "danger")
            return render_template("auth/register.html", form=form)

        user.roles.append(citizen_role)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"Welcome to Civic System, {user.first_name}!", "success")

        next_page = request.args.get("next")
        if next_page:
            parsed_url = urlsplit(next_page)
            if (
                next_page.startswith("/")
                and not next_page.startswith("//")
                and not parsed_url.netloc
                and not parsed_url.scheme
            ):
                return redirect(next_page)

        return redirect(url_for("citizen.index"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.has_role("admin"):
            return redirect(url_for("admin.dashboard"))
        
        return redirect(url_for("citizen.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash("Your account is currently inactive.", "danger")
                return render_template("auth/login.html", form=form)

            # Record the citizen's most recent successful login
            user.last_login_at = datetime.now(timezone.utc) + timedelta(hours=3)
            db.session.commit()

            login_user(user, remember=form.remember_me.data)

            # Clear password reset session data.
            session.pop("password_reset_user_id", None)
            session.pop("password_reset_expires", None)

            flash(f"Welcome back, {user.first_name}!", "success")

            # Redirect admin to their dashboard.
            if user.has_role("admin"):
                return redirect(url_for("admin.dashboard"))

            # Handle next page for ordinary users.
            next_page = request.args.get("next")
            if next_page:
                parsed_url = urlsplit(next_page)
                if (
                    next_page.startswith("/")
                    and not next_page.startswith("//")
                    and not parsed_url.netloc
                    and not parsed_url.scheme
                ):
                    return redirect(next_page)

            return redirect(url_for("citizen.index"))

        flash("Invalid email address or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()

    session.pop("password_reset_user_id", None)
    session.pop("password_reset_expires", None)

    return redirect(url_for("citizen.index"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
@limiter.limit("5 per 15 minutes", methods=["POST"], 
               deduct_when=lambda response: (response.headers.get("X-Password-Reset-Failed") == "1"))
def forgot_password():
    reset_user_id = session.get("password_reset_user_id")
    reset_expires = session.get("password_reset_expires")

    # Check whether the user has already verified their identity.
    if reset_user_id and reset_expires:
        if datetime.now(timezone.utc).timestamp() < reset_expires:
            form = PasswordResetForm()
            if form.validate_on_submit():
                user = db.session.get(User, reset_user_id)
                if not user:
                    session.pop("password_reset_user_id", None)
                    session.pop("password_reset_expires", None)
                    flash("Password reset session expired. Try again later.", "warning")
                    return redirect(url_for("auth.forgot_password"))

                user.set_password(form.password.data)
                db.session.commit()

                session.pop("password_reset_user_id", None)
                session.pop("password_reset_expires", None)

                flash("Password reset successfull. Please sign in.", "success")
                return redirect(url_for("auth.login"))

            return render_template(
                "auth/forgot_password.html",
                stage="reset",
                verification_form=None,
                reset_form=form,
            )

        # Verification session has expired.
        session.pop("password_reset_user_id", None)
        session.pop("password_reset_expires", None)

        flash("Password reset session expired. Verify your identity again.", "warning")

    # Stage 1: Verify email and National ID.
    form = PasswordResetVerificationForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        national_id = form.national_id.data.strip()
        user = User.query.filter_by(
            email=email,
            national_id=national_id,
        ).first()

        if user and user.is_active:
            session["password_reset_user_id"] = user.id
            session["password_reset_expires"] = (
                datetime.now(timezone.utc) + timedelta(minutes=10)
            ).timestamp()

            return redirect(url_for("auth.forgot_password"))

        # Use the same response regardless of which detail was incorrect.
        flash("Details couldn't be verified. Check them and try again.", "danger")

        response = make_response(
            render_template(
                "auth/forgot_password.html",
                stage="verify",
                verification_form=form,
                reset_form=None,
            )
        )

        # Flask-Limiter counts this as a failed verification attempt.
        response.headers["X-Password-Reset-Failed"] = "1"

        return response

    return render_template(
        "auth/forgot_password.html",
        stage="verify",
        verification_form=form,
        reset_form=None,
    )

