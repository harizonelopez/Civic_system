from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_required, current_user
from app.models import ServiceRequest, ApplicationRemark
from app.extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.before_request
def restrict_admin_access():
    # Require authentication first.
    if not current_user.is_authenticated:
        flash("Log in to access the administration portal.", "warning")
        return redirect(url_for("auth.login"))

    # Only administrators can access this area.
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
        flash("Access deinied for this route", "danger")
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
        flash("Permission denied to access this route", "danger")
        return redirect("/")

    applications = (
        ServiceRequest.query
        .order_by(ServiceRequest.submitted_at.desc())
        .all()
    )

    return render_template("admin/applications.html", applications=applications)


@admin_bp.route("/applications/<int:application_id>")
@login_required
def application_details(application_id):
    if not current_user.has_role("admin"):
        flash("Permission denied to access this route", "danger")
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
        flash("Select a valid application status.", "danger")
        return redirect(url_for("admin.application_details", application_id=application.id))

    if application.status == new_status:
        flash("Application already has that status.", "info")
        return redirect(url_for("admin.application_details", application_id=application.id))

    application.status = new_status
    db.session.commit()

    flash("Application status successfully updated.", "success")
    return redirect(url_for("admin.application_details", application_id=application.id))


@admin_bp.route("/applications/<int:application_id>/remarks", methods=["POST"])
@login_required
def add_application_remark(application_id):
    application = ServiceRequest.query.get_or_404(application_id)
    remark_text = request.form.get("remark", "").strip()

    if not remark_text:
        flash("Enter remark before submitting.", "warning")
        return redirect(url_for("admin.application_details", application_id=application.id))

    if len(remark_text) > 1000:
        flash("Remark cannot exceed 1,000 characters.", "danger")
        return redirect(url_for("admin.application_details", application_id=application.id))

    remark = ApplicationRemark(
        remark=remark_text,
        application=application,
        admin=current_user
    )

    db.session.add(remark)
    db.session.commit()

    flash("Remark successfully added.", "success")

    return redirect(url_for("admin.application_details", application_id=application.id))

