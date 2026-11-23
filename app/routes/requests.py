from flask import (
    Blueprint, render_template, abort,
    redirect, url_for, flash, current_app, request
)
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Service, ServiceRequest, ServiceOption
from app.forms.applications.business import (
    NewBusinessPermitForm,
    RenewBusinessPermitForm,
    AmendBusinessPermitForm,
)
from sqlalchemy.exc import SQLAlchemyError
import re

requests_bp = Blueprint("requests", __name__, url_prefix="/requests")

FEATURED_SERVICES = [
    {
        "name": "Business Permits",
        "slug": "business-permits",
        "category": "Business",
        "description": "Access business permit services, including applications for new "
                        "permits, renewals, amendments to business details, replacement "
                        "of lost or damaged permits, changes in business ownership, "
                        "and business permit cancellation or closure notifications.",
        "icon": "bi-shop",
        "processing": "Application service"
    },
    {
        "name": "Building Plan Approval",
        "slug": "building-plan-approval",
        "category": "Planning",
        "description": "Submit building plans and request the necessary development approvals.",
        "icon": "bi-building",
        "processing": "Application service"
    },
    {
        "name": "Public Health Services",
        "slug": "public-health-services",
        "category": "Public Health",
        "description": "Request health inspections and access applicable public health services.",
        "icon": "bi-heart-pulse",
        "processing": "Application service"
    },
    {
        "name": "Fire Safety Services",
        "slug": "fire-safety-services",
        "category": "Safety",
        "description": "Request fire safety inspections and relevant compliance services.",
        "icon": "bi-fire",
        "processing": "Application service"
    },
    {
        "name": "Waste Management",
        "slug": "waste-management",
        "category": "Environment",
        "description": "Access waste collection and environmental sanitation services.",
        "icon": "bi-recycle",
        "processing": "Service request"
    },
    {
        "name": "Market Services",
        "slug": "market-services",
        "category": "Trade",
        "description": "Submit requests related to market facilities, trading spaces and stall allocation.",
        "icon": "bi-shop-window",
        "processing": "Service request"
    }
]

@requests_bp.route("/")
def index():
    additional_services = (
        Service.query
        .filter_by(is_active=True)
        .order_by(Service.created_at.desc())
        .all()
    )

    return render_template(
        "services/index.html",
        featured_services=FEATURED_SERVICES,
        additional_services=additional_services
    )


@requests_bp.route("/featured/<slug>")
def featured_detail(slug):
    featured_service = next(
        (item for item in FEATURED_SERVICES if item["slug"] == slug), None
    )
    if featured_service is None:
        abort(404)

    database_service = None
    service_options = []

    # Business Permits is currently database-backed.
    if slug == "business-permits":
        database_service = Service.query.filter_by(
            code=slug,
            is_active=True
        ).first_or_404()

        service_options = [
            option
            for option in database_service.service_options
            if option.is_active
        ]

    return render_template(
        "services/featured-detail.html",
        service=featured_service,
        database_service=database_service,
        service_options=service_options
    )


@requests_bp.route("/featured/<slug>/apply/<option>", methods=["GET", "POST"])
@login_required
def apply_featured(slug, option):
    featured_service = next(
        (item for item in FEATURED_SERVICES if item["slug"] == slug), None)
    if featured_service is None:
        abort(404)

    # Map application option codes to their corresponding forms.
    application_forms = {
        "business-permits": {
            "new-permit": NewBusinessPermitForm,
            "renewal": RenewBusinessPermitForm,
            "amendment": AmendBusinessPermitForm,
        }
    }
    form_class = application_forms.get(slug, {}).get(option)
    if form_class is None:
        abort(404)

    # Retrieve the service from the database.
    database_service = Service.query.filter_by(
        code=slug,
        is_active=True
    ).first_or_404()

    # Retrieve the selected application option.
    database_option = ServiceOption.query.filter_by(
        service_id=database_service.id,
        code=option,
        is_active=True
    ).first_or_404()

    # Require a registered National ID for all service applications
    if not (current_user.national_id or "").strip():
        flash("Update your profile with your National ID before submitting a service application.", "warning")
        return redirect(url_for("citizen.edit_profile",
                                next=url_for("requests.apply_featured", 
                                             slug=slug, option=option)))

    form = form_class()
    if form.validate_on_submit():
        form_data = {
            name: field.data
            for name, field in form._fields.items()
            if name not in ("csrf_token", "submit")
        }
        if slug == "business-permits":
            form_data["owner_id_number"] = current_user.national_id
            
        # Preserve the service and option details at submission time.
        service_snapshot = {
            "service": {
                "id": database_service.id,
                "name": database_service.name,
                "code": database_service.code,
                "description": database_service.description,
                "department": database_service.department.name,
                "category": (
                    database_service.category.name
                    if database_service.category else None
                )
            },
            "option": {
                "id": database_option.id,
                "name": database_option.name,
                "code": database_option.code,
                "description": database_option.description,
                "fee": str(database_option.fee),
                "processing_days": database_option.processing_days,
                "eligibility": database_option.eligibility,
                "requirements": database_option.requirements
            }
        }
        application = ServiceRequest(
            title=f"{database_service.name} - {database_option.name}",
            description=database_option.description,
            service_slug=slug,
            option_code=option,
            form_data=form_data,
            service_snapshot=service_snapshot,
            citizen_id=current_user.id,
            service_id=database_service.id,
            service_option_id=database_option.id
        )
        try:
            db.session.add(application)
            db.session.commit()

            flash("Application submitted successfully.", "success")
            return redirect(url_for("requests.application_confirmation", reference_number=application.reference_number))
        except SQLAlchemyError:
            db.session.rollback()

            current_app.logger.exception("Application submission failed.")
            flash("Application submission failed. Please try again.", "danger")

    return render_template(
        "services/applications/apply.html",
        service=featured_service,
        database_service=database_service,
        database_option=database_option,
        option_label=database_option.name,
        form=form
    )


@requests_bp.route("/applications/<reference_number>/confirmation")
@login_required
def application_confirmation(reference_number):
    application = ServiceRequest.query.filter_by(
        reference_number=reference_number,
        citizen_id=current_user.id
    ).first_or_404()

    service = next(
        (
            item for item in FEATURED_SERVICES
            if item["slug"] == application.service_slug
        ),
        None
    )

    if service is None:
        abort(404)

    return render_template(
        "services/applications/confirmation.html",
        application=application,
        service=service,
    )


@requests_bp.route("/track", methods=["GET"])
@login_required
def track_application():
    reference_number = request.args.get(
        "reference_number", ""
    ).strip().upper()

    if not reference_number:
        return render_template("services/applications/track.html")

    # Accept only references in the expected format: CSR- + 12 hex characters
    if not re.fullmatch(r"CSR-[A-F0-9]{12}", reference_number):
        flash("Please enter a valid application reference number.", "warning")
        return redirect(url_for("requests.track_application"))

    application = ServiceRequest.query.filter_by(
        reference_number=reference_number,
        citizen_id=current_user.id
    ).first()

    if application is None:
        flash(
            "We couldn't find an application with that reference number in your account. "
            "Please check the number and try again.",
            "warning"
        )
        return redirect(url_for("requests.track_application"))

    return redirect(
        url_for(
            "requests.application_tracking_details",
            reference_number=application.reference_number
        )
    )


@requests_bp.route("/track/<reference_number>")
@login_required
def application_tracking_details(reference_number):
    application = ServiceRequest.query.filter_by(
        reference_number=reference_number.strip().upper(),
        citizen_id=current_user.id
    ).first()

    if application is None:
        flash(
            "We couldn't find an application with that reference number in your account. "
            "Please check the number and try again.",
            "warning"
        )
        return redirect(url_for("requests.track_application"))

    return render_template("services/applications/tracking-details.html", application=application,)


@requests_bp.route("/<int:service_id>")
def detail(service_id):
    service = Service.query.filter_by(
        id=service_id,
        is_active=True
    ).first_or_404()

    service_options = [
        option for option in service.service_options
        if option.is_active
    ]

    return render_template(
        "services/detail.html",
        service=service,
        service_options=service_options
    )


