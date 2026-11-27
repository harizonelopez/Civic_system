from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_required, current_user
from app.models import ServiceRequest, ApplicationRemark, User
from app.models.support_request import SupportRequest
from app.extensions import db
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from app.forms.auth import AdminCitizenForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.before_request
def restrict_admin_access():
    if not current_user.is_authenticated:
        flash("Login access denied.", "warning")
        return redirect(url_for("auth.login"))

    if not current_user.has_role("admin"):
        flash("Access denied.", "danger")
        return redirect("/")


@admin_bp.route("/")
def admin_home():
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if not current_user.has_role("admin"):
        flash("Access denied.", "danger")
        return redirect("/")

    total_applications = ServiceRequest.query.count()
    pending_applications = ServiceRequest.query.filter_by(
        status="submitted"
    ).count()

    processing_applications = ServiceRequest.query.filter_by(
        status="processing"
    ).count()

    approved_applications = ServiceRequest.query.filter_by(
        status="approved"
    ).count()

    rejected_applications = ServiceRequest.query.filter_by(
        status="rejected"
    ).count()

    recent_applications = (
        ServiceRequest.query
        .order_by(ServiceRequest.submitted_at.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        total_applications=total_applications,
        pending_applications=pending_applications,
        processing_applications=processing_applications,
        approved_applications=approved_applications,
        rejected_applications=rejected_applications,
        recent_applications=recent_applications
    )


@admin_bp.route("/applications")
@login_required
def applications():
    if not current_user.has_role("admin"):
        flash("Access denied", "danger")
        return redirect("/")

    applications = (
        ServiceRequest.query
        .order_by(ServiceRequest.submitted_at.desc())
        .all()
    )

    return render_template("admin/applications.html", applications=applications)


@admin_bp.route("/citizens")
@login_required
def citizens():
    citizens = (
        User.query
        .filter(User.roles.any(name="citizen"))
        .order_by(User.created_at.desc())
        .all()
    )

    return render_template("admin/citizens.html", citizens=citizens)


@admin_bp.route("/citizens/<int:citizen_id>")
@login_required
def citizen_details(citizen_id):
    citizen = (
        User.query
        .filter(
            User.id == citizen_id,
            User.roles.any(name="citizen")
        )
        .first_or_404()
    )

    applications = (
        ServiceRequest.query
        .filter_by(citizen_id=citizen.id)
        .order_by(ServiceRequest.submitted_at.desc())
        .all()
    )

    return render_template("admin/citizen-details.html", citizen=citizen, applications=applications)


@admin_bp.route("/citizens/<int:citizen_id>/edit", methods=["GET", "POST"])
@login_required
def edit_citizen(citizen_id):
    citizen = (
        User.query
        .filter(
            User.id == citizen_id,
            User.roles.any(name="citizen")
        )
        .first_or_404()
    )

    # Prevents editing already deleted user
    if citizen.email.endswith("@deleted.invalid"):
        flash("Deleted account can't be edited.", "danger")
        return redirect(url_for("admin.citizen_details", citizen_id=citizen.id))

    form = AdminCitizenForm(obj=citizen)
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        national_id = form.national_id.data.strip()

        phone_number = (
            form.phone_number.data.strip()
            if form.phone_number.data else None
        )

        existing_email = User.query.filter(
            db.func.lower(User.email) == email,
            User.id != citizen.id
        ).first()

        if existing_email:
            flash("Email address already taken.", "danger")
            return render_template("admin/edit-citizen.html", citizen=citizen, form=form)

        existing_id = User.query.filter(
            User.national_id == national_id,
            User.id != citizen.id
        ).first()

        if existing_id:
            flash("National ID already taken.", "danger")
            return render_template("admin/edit-citizen.html", citizen=citizen, form=form)

        if phone_number:
            existing_phone = User.query.filter(
                User.phone_number == phone_number,
                User.id != citizen.id
            ).first()

            if existing_phone:
                flash("Phone number already taken.", "danger")
                return render_template("admin/edit-citizen.html", citizen=citizen, form=form)

        citizen.first_name = form.first_name.data.strip()
        citizen.last_name = form.last_name.data.strip()
        citizen.email = email
        citizen.phone_number = phone_number
        citizen.national_id = national_id
        citizen.gender = form.gender.data

        db.session.commit()

        flash("Citizen details updated.", "success")
        return redirect(url_for("admin.citizen_details", citizen_id=citizen.id))

    if request.method == "GET":
        form.first_name.data = citizen.first_name
        form.last_name.data = citizen.last_name
        form.email.data = citizen.email
        form.phone_number.data = citizen.phone_number
        form.national_id.data = citizen.national_id
        form.gender.data = citizen.gender

    return render_template("admin/edit-citizen.html", citizen=citizen, form=form)


@admin_bp.route("/citizens/<int:citizen_id>/delete", methods=["GET", "POST"])
@login_required
def delete_citizen(citizen_id):
    citizen = (
        User.query
        .filter(
            User.id == citizen_id,
            User.roles.any(name="citizen")
        )
        .first_or_404()
    )

    if citizen.email.endswith("@deleted.invalid"):  # Prevent deleting an already deleted citizen account again
        flash("Citizen account already deleted.", "warning")
        return redirect(url_for("admin.citizen_details", citizen_id=citizen.id))

    if request.method == "POST":
        # Preserve application records & audit history.
        # Anonymise personal information instead of deleting the database row-data
        citizen.first_name = "Deleted"
        citizen.last_name = "Citizen"
        citizen.email = f"deleted_citizen_{citizen.id}@deleted.invalid"
        citizen.phone_number = None
        citizen.national_id = None
        citizen.gender = None

        citizen.is_active = False
        citizen.is_verified = False

        db.session.commit()
        flash("Account deleted & personal information anonymised.", "success")
        return redirect(url_for("admin.citizens"))

    return render_template("admin/delete-citizen.html", citizen=citizen)


@admin_bp.route("/citizens/<int:citizen_id>/toggle-status", methods=["POST"])
@login_required
def toggle_citizen_status(citizen_id):
    citizen = (
        User.query
        .filter(
            User.id == citizen_id,
            User.roles.any(name="citizen")
        )
        .first_or_404()
    )

    if citizen.email.endswith("@deleted.invalid"):  # Prevents deleted accounts from being reactivated
        flash("Deleted account can't be reactivated.", "danger")
        return redirect(url_for("admin.citizen_details", citizen_id=citizen.id))

    citizen.is_active = not citizen.is_active
    db.session.commit()

    if citizen.is_active:
        flash("Citizen account activated.", "success")
    else:
        flash("Citizen account deactivated.", "warning")

    return redirect(url_for("admin.citizen_details", citizen_id=citizen.id))


@admin_bp.route("/applications/<int:application_id>")
@login_required
def application_details(application_id):
    if not current_user.has_role("admin"):
        flash("Access denied.", "danger")
        return redirect("/")

    application = ServiceRequest.query.get_or_404(application_id)

    return render_template("admin/application-details.html", application=application)


@admin_bp.route("/applications/<int:application_id>/update-status", methods=["POST"])
@login_required
def update_application_status(application_id):
    if not current_user.has_role("admin"):
        flash("Permission denied to perform this action.", "danger")
        return redirect(url_for("admin.applications"))

    application = ServiceRequest.query.get_or_404(application_id)
    allowed_statuses = [
        "submitted",
        "processing",
        "approved",
        "completed",
        "rejected",
        "cancelled"
    ]

    new_status = request.form.get("status", "").strip().lower()
    if new_status not in allowed_statuses:
        flash("Select a valid status.", "danger")
        return redirect(url_for("admin.application_details", application_id=application.id))
      
    if application.status == new_status:
        flash("Application already has that status.", "info")
        return redirect(url_for("admin.application_details", application_id=application.id))

    application.status = new_status
    db.session.commit()

    flash("Application status updated.", "success")
    return redirect(url_for("admin.application_details", application_id=application.id))


@admin_bp.route("/applications/<int:application_id>/remarks", methods=["POST"])
@login_required
def add_application_remark(application_id):
    application = ServiceRequest.query.get_or_404(application_id)
    remark_text = request.form.get("remark", "").strip()

    if not remark_text:
        flash("Enter remark before submission.", "warning")
        return redirect(url_for("admin.application_details", application_id=application.id))

    if len(remark_text) > 500:
        flash("Remark can't exceed 500 characters.", "danger")
        return redirect(url_for("admin.application_details", application_id=application.id))

    remark = ApplicationRemark(
        remark=remark_text,
        application=application,
        admin=current_user
    )

    db.session.add(remark)
    db.session.commit()

    flash("Remark added.", "success")
    return redirect(url_for("admin.application_details", application_id=application.id))


@admin_bp.route("/support-requests")
@login_required
def support_requests():
    support_requests = (
        SupportRequest.query
        .order_by(SupportRequest.submitted_at.desc())
        .all()
    )

    return render_template("admin/support-requests.html", support_requests=support_requests)


@admin_bp.route("/support-requests/<int:request_id>", methods=["GET", "POST"])
@login_required
def support_request_details(request_id):
    support_request = SupportRequest.query.get_or_404(request_id)

    if request.method == "POST":
        response = request.form.get("admin_response", "").strip()
        status = request.form.get("status", "").strip().lower()

        allowed_statuses = [
            "submitted",
            "in_progress",
            "resolved"
        ]

        if status not in allowed_statuses:
            flash("Select a valid status.", "danger")
            return redirect(url_for("admin.support_request_details", request_id=support_request.id))
      
        now = datetime.now(timezone.utc)

        support_request.admin_response = response or None
        support_request.status = status

        if status == "resolved":
            if support_request.resolved_at is None:
                support_request.resolved_at = now
        else:
            support_request.resolved_at = None

        support_request.updated_at = now

        db.session.commit()
        flash("Request updated.", "success")
        return redirect(url_for("admin.support_request_details", request_id=support_request.id))

    return render_template("admin/support-request-details.html", support_request=support_request)
