from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from app.extensions import db
from app.forms.support import SupportRequestForm
from app.models.support_request import SupportRequest
from app.models.service_request import ServiceRequest


support_bp = Blueprint("support", __name__, url_prefix="/support")


@support_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = SupportRequestForm()
    # Prefill & enforce account details for logged-in citizens.
    if current_user.is_authenticated:
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email

    if form.validate_on_submit():
        application_reference = (
            form.application_reference.data.strip()
            if form.application_reference.data
            else None
        )

        # Ensure a logged-in citizen can only reference their own application.
        if application_reference and current_user.is_authenticated:
            application = ServiceRequest.query.filter_by(
                reference_number=application_reference,
                citizen_id=current_user.id
            ).first()

            if application is None:
                form.application_reference.errors.append(
                    "We couldn't find an application with that reference "
                    "in your account."
                )

                return render_template(
                    "support/contact.html",
                    form=form
                )

        support_request = SupportRequest(
            citizen_id=(
                current_user.id
                if current_user.is_authenticated
                else None
            ),
            full_name=(
                current_user.full_name
                if current_user.is_authenticated
                else form.full_name.data.strip()
            ),
            email=(
                current_user.email
                if current_user.is_authenticated
                else form.email.data.strip().lower()
            ),
            category=form.category.data,
            subject=form.subject.data.strip(),
            application_reference=application_reference,
            message=form.message.data.strip()
        )

        try:
            db.session.add(support_request)
            db.session.commit()

            flash(
                f"Support request was submitted successfully. "
                f"Your reference number is {support_request.reference_number}.",
                "success"
            )

            return redirect(url_for("support.contact"))

        except Exception:
            db.session.rollback()
            flash(
                "We couldn't submit your request. Please try again.",
                "danger"
            )

    return render_template(
        "support/contact.html",
        form=form
    )

