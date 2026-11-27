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


def seed_building_plan_approval():
    # 1. Create or retrieve the department.
    department = Department.query.filter_by(code="PLN").first()
    if department is None:
        department = Department(
            name="Physical Planning",
            code="PLN",
            description=(
                "Responsible for physical planning, development control "
                "and building plan assessments."
            )
        )
        db.session.add(department)
        db.session.flush()

    # 2. Create or retrieve the service category.
    category = ServiceCategory.query.filter_by(name="Planning").first()
    if category is None:
        category = ServiceCategory(
            name="Planning",
            description=(
                "Building plans, development applications "
                "and physical planning services."
            )
        )
        db.session.add(category)
        db.session.flush()

    # 3. Create or retrieve the main service.
    service = Service.query.filter_by(
        code="building-plan-approval"
    ).first()

    if service is None:
        service = Service(
            name="Building Plan Approval",
            code="building-plan-approval",
            description=(
                "Submit proposed building plans for technical assessment "
                "and approval before construction begins."
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

    # 4. Define the application options.
    options = [
        {
            "name": "New Building Plan Approval",
            "code": "new-plan",
            "description": (
                "Submit building plans for technical assessment "
                "and approval before starting a new construction project."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Proof of land ownership or consent from the landowner.\n"
                "3. Certificate of official search or title deed.\n"
                "4. Architectural building plans prepared and signed "
                "by a registered architect.\n"
                "5. Structural drawings and calculations, where applicable.\n"
                "6. Survey plan or site location details.\n"
                "7. Other supporting documents required by the county."
            ),
            "eligibility": (
                "Landowners or their authorized representatives "
                "proposing new construction within the county, "
                "subject to applicable planning and building regulations."
            ),
            "processing_days": 30,
            "fee": Decimal("1000.00")
        },
        {
            "name": "Revised Building Plans",
            "code": "revised-plan",
            "description": (
                "Submit amended building plans for assessment where "
                "changes have been made to previously submitted or "
                "approved construction designs."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Previous building plan approval reference, where applicable.\n"
                "3. Previously approved building plans, where applicable.\n"
                "4. Revised architectural drawings.\n"
                "5. Updated structural drawings and calculations, "
                "where applicable.\n"
                "6. Description of the proposed changes.\n"
                "7. Other supporting documents required by the county."
            ),
            "eligibility": (
                "Landowners or authorized representatives seeking "
                "approval of changes to previously submitted or "
                "approved building plans."
            ),
            "processing_days": 21,
            "fee": Decimal("5000.00")
        },
        {
            "name": "Building Plan Resubmission",
            "code": "plan-resubmission",
            "description": (
                "Resubmit building plans after addressing corrections, "
                "comments or deficiencies identified during the "
                "county's technical assessment."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Previous application reference number.\n"
                "3. Updated building plans incorporating the requested corrections.\n"
                "4. Response or explanation addressing the review comments.\n"
                "5. Supporting technical documents, where applicable."
            ),
            "eligibility": (
                "Applicants whose building plan submissions require "
                "corrections or additional information following "
                "a county technical review."
            ),
            "processing_days": 14,
            "fee": Decimal("0.00")
        },
        {
            "name": "Building Plan Extension",
            "code": "plan-extension",
            "description": (
                "Request an extension of the validity period of previously "
                "approved building plans where construction has not "
                "commenced or remains incomplete."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Previous building plan approval reference.\n"
                "3. Copy of the existing building plan approval.\n"
                "4. Explanation for the extension request.\n"
                "5. Current construction status, where applicable.\n"
                "6. Other supporting documents required by the county."
            ),
            "eligibility": (
                "Holders of previously approved building plans seeking "
                "an extension, subject to the applicable county rules "
                "and approval conditions."
            ),
            "processing_days": 7,
            "fee": Decimal("5000.00")
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

    print("\nBuilding Plan Approval data seeded successfully.")
    print(f"Department: {department.name}")
    print(f"Category: {category.name}")
    print(f"Service: {service.name}")

    print("\nAvailable application options:")

    for option in service.service_options:
        if option.is_active:
            print(f"- {option.name} ({option.code})")


def seed_public_health_services():
    # 1. Create or retrieve the department.
    department = Department.query.filter_by(code="HLT").first()
    if department is None:
        department = Department(
            name="Public Health",
            code="HLT",
            description=(
                "Responsible for public health inspections, food safety, "
                "sanitation and environmental health services."
            )
        )
        db.session.add(department)
        db.session.flush()

    # 2. Create or retrieve the service category.
    category = ServiceCategory.query.filter_by(name="Public Health").first()
    if category is None:
        category = ServiceCategory(
            name="Public Health",
            description=(
                "Food hygiene, health inspections, sanitation "
                "and public health services."
            )
        )
        db.session.add(category)
        db.session.flush()

    # 3. Create or retrieve the main service.
    service = Service.query.filter_by(
        code="public-health-services"
    ).first()

    if service is None:
        service = Service(
            name="Public Health Services",
            code="public-health-services",
            description=(
                "Access public health services including food hygiene "
                "inspections, food handler certification, premises "
                "inspections and reporting of public health concerns."
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

    # 4. Define the application options.
    options = [
        {
            "name": "Food Hygiene Inspection",
            "code": "food-hygiene-inspection",
            "description": (
                "Request a food hygiene inspection to assess whether "
                "food premises meet applicable public health and "
                "food safety requirements."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Business name and registration details, where applicable.\n"
                "3. Physical location of the food premises.\n"
                "4. Business permit, where applicable.\n"
                "5. Details of the food handling activities.\n"
                "6. Previous inspection report, where applicable."
            ),
            "eligibility": (
                "Owners, operators or authorized representatives "
                "of food businesses and food handling premises "
                "within the county."
            ),
            "processing_days": 5,
            "fee": Decimal("600.00")
        },
        {
            "name": "Food Handler Medical Certificate",
            "code": "food-handler-certificate",
            "description": (
                "Apply for a food handler medical examination and "
                "certification in accordance with applicable "
                "public health requirements."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Applicant's full name and contact details.\n"
                "3. Recent passport-size photograph, where required.\n"
                "4. Name and location of the employer or food premises.\n"
                "5. Medical examination details, where applicable."
            ),
            "eligibility": (
                "Individuals involved in the preparation, handling, "
                "storage or sale of food within the county."
            ),
            "processing_days": 3,
            "fee": Decimal("400.00")
        },
        {
            "name": "Public Health Premises Inspection",
            "code": "premises-inspection",
            "description": (
                "Request a public health inspection of business, "
                "residential or other premises to assess sanitation, "
                "hygiene and environmental health conditions."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Applicant's contact information.\n"
                "3. Physical location of the premises.\n"
                "4. Type and intended use of the premises.\n"
                "5. Reason for requesting the inspection.\n"
                "6. Previous inspection report, where applicable."
            ),
            "eligibility": (
                "Property owners, tenants, business operators "
                "or authorized representatives requesting "
                "a public health inspection."
            ),
            "processing_days": 5,
            "fee": Decimal("1500.00")
        },
        {
            "name": "Public Health Complaint",
            "code": "public-health-complaint",
            "description": (
                "Report sanitation, hygiene or environmental health "
                "concerns that may pose a risk to the public."
            ),
            "requirements": (
                "1. Description of the reported public health concern.\n"
                "2. Location of the affected premises or area.\n"
                "3. Date or period when the issue was observed.\n"
                "4. Supporting photographs or evidence, where available.\n"
                "5. Contact details for follow-up, where applicable."
            ),
            "eligibility": (
                "Any member of the public reporting a suspected "
                "public health or sanitation concern within the county."
            ),
            "processing_days": 3,
            "fee": Decimal("0.00")
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

    print("\nPublic Health Services data seeded successfully.")
    print(f"Department: {department.name}")
    print(f"Category: {category.name}")
    print(f"Service: {service.name}")

    print("\nAvailable application options:")

    for option in service.service_options:
        if option.is_active:
            print(f"- {option.name} ({option.code})")


def seed_fire_safety_services():
    # 1. Create or retrieve the department.
    department = Department.query.filter_by(code="FIR").first()
    if department is None:
        department = Department(
            name="Fire and Rescue Services",
            code="FIR",
            description=(
                "Responsible for fire prevention, fire safety inspections, "
                "emergency preparedness and fire response services."
            )
        )
        db.session.add(department)
        db.session.flush()

    # 2. Create or retrieve the service category.
    category = ServiceCategory.query.filter_by(
        name="Fire Safety"
    ).first()

    if category is None:
        category = ServiceCategory(
            name="Fire Safety",
            description=(
                "Fire safety inspections, certification, "
                "compliance and public fire hazard reporting."
            )
        )
        db.session.add(category)
        db.session.flush()

    # 3. Create or retrieve the main service.
    service = Service.query.filter_by(
        code="fire-safety-services"
    ).first()

    if service is None:
        service = Service(
            name="Fire Safety Services",
            code="fire-safety-services",
            description=(
                "Access fire safety inspections, certification, "
                "follow-up assessments and reporting of fire hazards "
                "within the county."
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

    # 4. Define the application options.
    options = [
        {
            "name": "Fire Safety Inspection",
            "code": "fire-safety-inspection",
            "description": (
                "Request a fire safety inspection of commercial or "
                "public premises to assess fire prevention measures, "
                "emergency exits and firefighting equipment. "
                "Fees vary depending on premises type and size."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Business name and registration details, where applicable.\n"
                "3. Physical location of the premises.\n"
                "4. Business permit, where applicable.\n"
                "5. Type and approximate size of the premises.\n"
                "6. Details of existing firefighting equipment.\n"
                "7. Previous inspection report, where applicable."
            ),
            "eligibility": (
                "Property owners, business operators or authorized "
                "representatives responsible for premises within the county."
            ),
            "processing_days": 5,
            "fee": Decimal("1500.00")
        },
        {
            "name": "Fire Safety Certificate",
            "code": "fire-safety-certificate",
            "description": (
                "Apply for fire safety compliance assessment and "
                "certification after meeting applicable fire safety "
                "requirements. Fees depend on the premises category "
                "and applicable annual compliance charges."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Business permit, where applicable.\n"
                "3. Physical location of the premises.\n"
                "4. Previous fire safety inspection report, where applicable.\n"
                "5. Details of installed firefighting equipment.\n"
                "6. Evidence of corrective measures, where applicable.\n"
                "7. Other documents required during assessment."
            ),
            "eligibility": (
                "Owners or authorized operators of commercial and "
                "public premises seeking fire safety compliance assessment."
            ),
            "processing_days": 5,
            "fee": Decimal("3000.00")
        },
        {
            "name": "Fire Safety Re-inspection",
            "code": "fire-safety-reinspection",
            "description": (
                "Request a follow-up inspection after addressing "
                "fire safety issues identified during an earlier "
                "assessment. Additional inspection charges may apply."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Previous inspection reference or report.\n"
                "3. Physical location of the premises.\n"
                "4. Description of corrective measures completed.\n"
                "5. Supporting photographs or documents, where available."
            ),
            "eligibility": (
                "Applicants whose premises were previously inspected "
                "and require follow-up assessment."
            ),
            "processing_days": 3,
            "fee": Decimal("1000.00")
        },
        {
            "name": "Fire Safety Complaint",
            "code": "fire-safety-complaint",
            "description": (
                "Report potential fire hazards, blocked emergency exits, "
                "unsafe electrical installations or inadequate "
                "fire prevention measures within the county."
            ),
            "requirements": (
                "1. Description of the reported fire safety concern.\n"
                "2. Location of the affected premises or area.\n"
                "3. Date or period when the issue was observed.\n"
                "4. Supporting photographs or evidence, where available.\n"
                "5. Contact details for follow-up, where applicable."
            ),
            "eligibility": (
                "Any member of the public reporting a suspected "
                "fire hazard or fire safety concern within the county."
            ),
            "processing_days": 2,
            "fee": Decimal("0.00")
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

    print("\nFire Safety Services data seeded successfully.")
    print(f"Department: {department.name}")
    print(f"Category: {category.name}")
    print(f"Service: {service.name}")

    print("\nAvailable application options:")

    for option in service.service_options:
        if option.is_active:
            print(f"- {option.name} ({option.code})")


def seed_waste_management_services():
    # 1. Create or retrieve the department.
    department = Department.query.filter_by(code="ENV").first()
    if department is None:
        department = Department(
            name="Environment and Waste Management",
            code="ENV",
            description=(
                "Responsible for environmental conservation, "
                "waste collection, disposal, sanitation and "
                "environmental cleanliness within the county."
            )
        )
        db.session.add(department)
        db.session.flush()

    # 2. Create or retrieve the service category.
    category = ServiceCategory.query.filter_by(name="Environment").first()
    if category is None:
        category = ServiceCategory(
            name="Environment",
            description=(
                "Waste collection, environmental sanitation, "
                "waste disposal and reporting of environmental concerns."
            )
        )
        db.session.add(category)
        db.session.flush()

    # 3. Create or retrieve the main service.
    service = Service.query.filter_by(code="waste-management").first()
    if service is None:
        service = Service(
            name="Waste Management",
            code="waste-management",
            description=(
                "Access household and commercial waste collection, "
                "bulk waste removal, environmental sanitation "
                "and waste-related reporting services."
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

    # 4. Define the application options.
    options = [
        {
            "name": "Household Waste Collection",
            "code": "household-waste-collection",
            "description": (
                "Request scheduled waste collection services "
                "for residential properties and households "
                "within the county."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Residential address and physical location.\n"
                "3. Ward and area of residence.\n"
                "4. Contact phone number.\n"
                "5. Preferred collection schedule, where applicable."
            ),
            "eligibility": (
                "Residents, tenants, landlords and property owners "
                "within the county."
            ),
            "processing_days": 3,
            "fee": Decimal("600.00")
        },
        {
            "name": "Commercial Waste Collection",
            "code": "commercial-waste-collection",
            "description": (
                "Request waste collection services for shops, offices, "
                "restaurants, institutions and other commercial premises. "
                "Charges may depend on the nature and volume of waste."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Business name and registration details, where applicable.\n"
                "3. Physical location of the premises.\n"
                "4. Ward and area of operation.\n"
                "5. Type and estimated volume of waste generated.\n"
                "6. Contact phone number."
            ),
            "eligibility": (
                "Business owners, institutions and authorized "
                "operators of commercial premises within the county."
            ),
            "processing_days": 5,
            "fee": Decimal("1500.00")
        },
        {
            "name": "Bulk Waste Collection",
            "code": "bulk-waste-collection",
            "description": (
                "Request collection and disposal of bulky waste materials "
                "from residential, commercial or institutional premises. "
                "Charges may depend on the quantity and type of waste."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Physical location of the waste.\n"
                "3. Description and estimated quantity of waste.\n"
                "4. Type of waste requiring collection.\n"
                "5. Preferred collection date.\n"
                "6. Contact phone number."
            ),
            "eligibility": (
                "Residents, property owners, businesses and institutions "
                "requiring bulk waste collection within the county."
            ),
            "processing_days": 5,
            "fee": Decimal("0.00")
        },
        {
            "name": "Illegal Dumping Report",
            "code": "illegal-dumping-report",
            "description": (
                "Report illegal dumping, unauthorized waste disposal "
                "or accumulation of waste in public spaces requiring "
                "county investigation and intervention."
            ),
            "requirements": (
                "1. Location of the illegal dumping site.\n"
                "2. Description of the dumping incident.\n"
                "3. Date or approximate period when it was observed.\n"
                "4. Supporting photographs, where available.\n"
                "5. Contact details for follow-up, where applicable."
            ),
            "eligibility": (
                "Any member of the public reporting illegal "
                "waste disposal within the county."
            ),
            "processing_days": 3,
            "fee": Decimal("0.00")
        },
        {
            "name": "Environmental Sanitation Request",
            "code": "environmental-sanitation-request",
            "description": (
                "Submit requests for environmental cleaning, removal "
                "of accumulated waste, sanitation interventions "
                "and cleaning of public spaces."
            ),
            "requirements": (
                "1. Location of the affected area.\n"
                "2. Ward and name of the locality.\n"
                "3. Description of the sanitation concern.\n"
                "4. Supporting photographs, where available.\n"
                "5. Contact details for follow-up, where applicable."
            ),
            "eligibility": (
                "Residents, businesses, community representatives "
                "and institutions within the county."
            ),
            "processing_days": 5,
            "fee": Decimal("0.00")
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

    print("\nWaste Management data seeded successfully.")
    print(f"Department: {department.name}")
    print(f"Category: {category.name}")
    print(f"Service: {service.name}")

    print("\nAvailable application options:")

    for option in service.service_options:
        if option.is_active:
            print(f"- {option.name} ({option.code})")


def seed_market_services():
    # 1. Create or retrieve the department.
    department = Department.query.filter_by(code="MKT").first()
    if department is None:
        department = Department(
            name="Markets and Trade Services",
            code="MKT",
            description=(
                "Responsible for market administration, allocation "
                "of trading spaces, market facilities, sanitation "
                "and management of public markets within the county."
            )
        )
        db.session.add(department)
        db.session.flush()

    # 2. Create or retrieve the service category.
    category = ServiceCategory.query.filter_by(name="Market Services").first()
    if category is None:
        category = ServiceCategory(
            name="Market Services",
            description=(
                "Market stall applications, tenancy management, "
                "facility maintenance, sanitation and public "
                "market-related requests."
            )
        )
        db.session.add(category)
        db.session.flush()

    # 3. Create or retrieve the main service.
    service = Service.query.filter_by(code="market-services").first()
    if service is None:
        service = Service(
            name="Market Services",
            code="market-services",
            description=(
                "Access market stall allocation, tenancy management, "
                "market facility maintenance, sanitation and "
                "other public market services."
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

    # 4. Define the application options.
    options = [
        {
            "name": "Market Stall Application",
            "code": "stall-application",
            "description": (
                "Apply for an available market stall or designated "
                "trading space within a county-managed market. "
                "Allocation depends on availability and eligibility."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Applicant's full name and contact details.\n"
                "3. Preferred market and trading location.\n"
                "4. Type of goods or business to be operated.\n"
                "5. Preferred stall or trading space, where applicable.\n"
                "6. Business registration details, where applicable."
            ),
            "eligibility": (
                "Individuals, traders and business operators "
                "seeking an available county-managed market stall."
            ),
            "processing_days": 3,
            "fee": Decimal("1000.00")
        },
        {
            "name": "Market Stall Renewal",
            "code": "stall-renewal",
            "description": (
                "Submit a request to renew an existing market "
                "stall tenancy or trading space allocation."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Existing stall allocation or tenancy reference.\n"
                "3. Name and location of the market.\n"
                "4. Stall or trading space number.\n"
                "5. Previous payment receipts, where applicable.\n"
                "6. Current contact information."
            ),
            "eligibility": (
                "Existing market stall tenants and authorized "
                "traders holding a county market allocation."
            ),
            "processing_days": 3,
            "fee": Decimal("700.00")
        },
        {
            "name": "Market Stall Transfer",
            "code": "stall-transfer",
            "description": (
                "Request an authorized transfer or change of "
                "an existing market stall allocation or tenancy, "
                "subject to county approval."
            ),
            "requirements": (
                "1. Copy of National ID or passport.\n"
                "2. Existing stall allocation reference.\n"
                "3. Current stall number and market location.\n"
                "4. Reason for the requested transfer.\n"
                "5. Details of the proposed new allocation, where applicable.\n"
                "6. Supporting authorization documents, where applicable."
            ),
            "eligibility": (
                "Existing market stall tenants seeking an "
                "authorized change of stall allocation or tenancy."
            ),
            "processing_days": 2,
            "fee": Decimal("1500.00")
        },
        {
            "name": "Market Facility Maintenance Request",
            "code": "facility-maintenance",
            "description": (
                "Report damaged market facilities or request "
                "maintenance of stalls, drainage systems, roofs, "
                "water points, lighting and other county-managed "
                "market infrastructure."
            ),
            "requirements": (
                "1. Name and location of the affected market.\n"
                "2. Stall number or facility location, where applicable.\n"
                "3. Description of the maintenance issue.\n"
                "4. Photographs of the damage, where available.\n"
                "5. Contact details for follow-up."
            ),
            "eligibility": (
                "Market traders, stall tenants, market representatives "
                "and other members of the public."
            ),
            "processing_days": 4,
            "fee": Decimal("500.00")
        },
        {
            "name": "Market Sanitation Request",
            "code": "market-sanitation",
            "description": (
                "Request cleaning, waste removal, drainage clearing "
                "or other sanitation interventions within public "
                "market facilities."
            ),
            "requirements": (
                "1. Name and location of the affected market.\n"
                "2. Description of the sanitation concern.\n"
                "3. Specific affected area, where applicable.\n"
                "4. Supporting photographs, where available.\n"
                "5. Contact details for follow-up."
            ),
            "eligibility": (
                "Market traders, stall tenants, market representatives "
                "and members of the public."
            ),
            "processing_days": 2,
            "fee": Decimal("300.00")
        },
        {
            "name": "Market Complaint",
            "code": "market-complaint",
            "description": (
                "Submit complaints concerning market operations, "
                "unauthorized trading spaces, unfair stall allocation, "
                "market management or other issues affecting traders."
            ),
            "requirements": (
                "1. Name and location of the affected market.\n"
                "2. Description of the complaint.\n"
                "3. Date or approximate period of the incident.\n"
                "4. Supporting evidence, where available.\n"
                "5. Contact details for follow-up, where applicable."
            ),
            "eligibility": (
                "Market traders, stall tenants, business operators "
                "and members of the public."
            ),
            "processing_days": 1,
            "fee": Decimal("200.00")
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

    print("\nMarket Services data seeded successfully.")
    print(f"Department: {department.name}")
    print(f"Category: {category.name}")
    print(f"Service: {service.name}")

    print("\nAvailable application options:")

    for option in service.service_options:
        if option.is_active:
            print(f"- {option.name} ({option.code})")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        try:
            seed_business_permits()
            seed_building_plan_approval()
            seed_public_health_services()
            seed_fire_safety_services()
            seed_waste_management_services()
            seed_market_services()
        except Exception:
            db.session.rollback()
            raise        
        finally:
            db.session.remove()
            
