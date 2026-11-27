from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Service, ServiceRequest
from app.models.user import User
from app.forms.auth import ProfileForm, ChangePasswordForm

citizen_bp = Blueprint("citizen", __name__)


@citizen_bp.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.has_role("admin"):
            return redirect(url_for("admin.dashboard"))        
        if current_user.has_role("citizen"):
            return redirect(url_for("citizen.dashboard"))

    services = (
        Service.query
        .filter_by(is_active=True)
        .order_by(Service.created_at.desc())
        .limit(6)
        .all()
    )

    return render_template("index.html", services=services)


@citizen_bp.route("/dashboard")
@login_required
def dashboard():
    # Retrieve the citizen's applications.
    applications = (
        ServiceRequest.query
        .filter_by(citizen_id=current_user.id)
        .order_by(ServiceRequest.submitted_at.desc())
        .all()
    )

    total_applications = len(applications)
    completed_applications = sum(
        1 for application in applications
        if application.status == "completed"
    )
    pending_applications = sum(
        1 for application in applications
        if application.status not in ("completed", "rejected", "cancelled")
    )
    recent_applications = applications[:5]

    return render_template(
        "citizen/dashboard.html",
        total_applications=total_applications,
        pending_applications=pending_applications,
        completed_applications=completed_applications,
        recent_applications=recent_applications,
    )


@citizen_bp.route("/applications")
@login_required
def applications():
    applications = (
        ServiceRequest.query
        .filter_by(citizen_id=current_user.id)
        .order_by(ServiceRequest.submitted_at.desc())
        .all()
    )

    return render_template("citizen/applications.html", applications=applications)


@citizen_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    password_form = ChangePasswordForm()
    next_page = request.args.get("next")

    # Handle password changes independently.
    if password_form.change_password.data and password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            password_form.current_password.errors.append("Incorrect current password.")
        elif current_user.check_password(password_form.new_password.data):
            password_form.new_password.errors.append("New password must be different from the current password.")
        else:
            try:
                current_user.set_password(password_form.new_password.data)
                db.session.commit()
                flash("Password change successfull.", "success")
                return redirect(url_for("citizen.dashboard"))
            except Exception:
                db.session.rollback()
                current_app.logger.exception("Password change failed.")
                flash("Unable to update password. Try again.", "danger")

        return render_template(
            "citizen/edit_profile.html",
            form=form,
            password_form=password_form,
        )

    # Handle profile updates independently.
    if form.submit.data and form.validate_on_submit():
        national_id = form.national_id.data.strip()
        phone_number = (
            form.phone_number.data.strip()
            if form.phone_number.data
            else None
        )

        existing_id = User.query.filter(
            User.national_id == national_id,
            User.id != current_user.id
        ).first()

        if existing_id:
            form.national_id.errors.append(
                "National ID already registered with another account."
            )
            return render_template(
                "citizen/edit_profile.html",
                form=form,
                password_form=password_form,
            )

        if phone_number:
            existing_phone = User.query.filter(
                User.phone_number == phone_number,
                User.id != current_user.id
            ).first()

            if existing_phone:
                form.phone_number.errors.append(
                    "Phone number already registered with another account."
                )
                return render_template(
                    "citizen/edit_profile.html",
                    form=form,
                    password_form=password_form,
                )

        current_user.first_name = form.first_name.data.strip()
        current_user.last_name = form.last_name.data.strip()
        current_user.phone_number = phone_number
        current_user.national_id = national_id
        current_user.gender = form.gender.data

        try:
            db.session.commit()
            flash("Profile details update successfull.", "success")

            if (
                next_page
                and next_page.startswith("/")
                and not next_page.startswith("//")
            ):
                return redirect(next_page)

            return redirect(url_for("citizen.dashboard"))

        except Exception:
            db.session.rollback()
            current_app.logger.exception("Profile update failed.")
            flash("Unable to update your profile. Try again.", "danger")

    return render_template(
        "citizen/edit_profile.html",
        form=form,
        password_form=password_form,
    )


