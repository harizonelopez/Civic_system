import sys
from pathlib import Path
from decimal import Decimal

# Add the project root to Python's import path.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.extensions import db
from app.models import Department, ServiceCategory, Service, ServiceOption


def seed_business_permits():

    # 1. Create or retrieve the department.
    department = Department.query.filter_by(code="BUS").first()

    if department is None:
        department = Department(
            name="Business Services",
            code="BUS",
            description="Responsible for business-related public services."
        )
        db.session.add(department)
        db.session.flush()

    # 2. Create or retrieve the service category.
    category = ServiceCategory.query.filter_by(name="Business").first()

    if category is None:
        category = ServiceCategory(
            name="Business",
            description="Business registration, permits and related services."
        )
        db.session.add(category)
        db.session.flush()

    # 3. Create or retrieve the main service.
    service = Service.query.filter_by(code="business-permits").first()

    if service is None:
        service = Service(
            name="Business Permits",
            code="business-permits",
            description=(
                "Apply for a new business permit, renew an existing permit, "
                "or request amendments to business details."
            ),
            department=department,
            category=category,
            fee=Decimal("0.00"),
            processing_days=None,
            is_online=True,
            is_active=True
        )
        db.session.add(service)
        db.session.flush()
    
    # 4. Define the available application options.
    options = [
        {
            "name": "New Business Permit",
            "code": "new-permit",
            "description": (
                "Apply for a new permit to operate a business within the county."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Business registration certificate, where applicable.\n"
                "3. KRA PIN certificate.\n"
                "4. Physical business premises address.\n"
                "5. Lease agreement or proof of occupancy, where applicable.\n"
                "6. Additional sector-specific licences, where required."
            ),
            "eligibility": (
                "Individuals or registered entities intending to operate "
                "a business within the county, subject to applicable "
                "business and premises requirements."
            ),
            "processing_days": 5,
            "fee": Decimal("5000.00")
        },
        {
            "name": "Business Permit Renewal",
            "code": "renewal",
            "description": (
                "Renew an existing business permit for another operating period."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Existing business permit.\n"
                "3. Business registration details.\n"
                "4. Current business premises address.\n"
                "5. Updated contact information."
            ),
            "eligibility": (
                "Existing business permit holders seeking to renew "
                "their permits for a new operating period."
            ),
            "processing_days": 3,
            "fee": Decimal("3000.00")
        },
        {
            "name": "Amend Business Details",
            "code": "amendment",
            "description": (
                "Request changes to registered business or permit information."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Existing business permit.\n"
                "3. Details of the requested amendment.\n"
                "4. Supporting documents depending on the amendment, "
                "such as ownership or business name change documents."
            ),
            "eligibility": (
                "Existing business permit holders or their authorized "
                "representatives requesting changes to registered "
                "business information."
            ),
            "processing_days": 2,
            "fee": Decimal("1000.00")
        }
    ]

    # 5. Create or update the available options.
    for item in options:
        option = ServiceOption.query.filter_by(
            code=item["code"],
            service=service
        ).first()

        if option is None:
            option = ServiceOption(
                code=item["code"],
                service=service
            )
            db.session.add(option)

        option.name = item["name"]
        option.description = item["description"]
        option.requirements = item["requirements"]
        option.eligibility = item["eligibility"]
        option.processing_days = item["processing_days"]
        option.fee = item["fee"]
        option.is_active = True

    # 6. Save all records.
    db.session.commit()

    print("\nBusiness Permits data seeded successfully.")
    print(f"Department: {department.name}")
    print(f"Category: {category.name}")
    print(f"Service: {service.name}")

    print("\nAvailable application options:")

    for option in service.service_options:
        print(f"- {option.name} ({option.code})")


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        try:
            seed_business_permits()
        except Exception:
            db.session.rollback()
            raise
        
        finally:
            db.session.remove()
