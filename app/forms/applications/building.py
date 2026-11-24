from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    IntegerField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    NumberRange,
)

# Kenyan mobile numbers.
KENYAN_PHONE = r"^(?:07|01)\d{8}$"

# Text fields containing letters, numbers and common punctuation.
TEXT_WITH_LETTERS = (
    r"^(?=.*[A-Za-z])[A-Za-zÀ-ÿ0-9\s&'().,/ -]+$"
)

# Property and approval reference numbers.
REFERENCE_NUMBER = r"^[A-Za-z0-9/-]+$"

# Reusable property and contact information.
class BuildingPlanBaseForm(FlaskForm):
    property_location = StringField(
        "Property Location",
        validators=[
            DataRequired(),
            Length(min=3, max=180),
            Regexp(
                TEXT_WITH_LETTERS,
                message="Enter a valid property location."
            )
        ]
    )
    ward = StringField(
        "Ward",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
            Regexp(
                TEXT_WITH_LETTERS,
                message="Enter a valid ward name."
            )
        ]
    )
    plot_number = StringField(
        "Plot / Land Reference Number",
        validators=[
            DataRequired(),
            Length(min=2, max=60),
            Regexp(
                REFERENCE_NUMBER,
                message="Enter a valid plot or land reference number."
            )
        ]
    )
    contact_phone = StringField(
        "Contact Number",
        validators=[
            DataRequired(),
            Regexp(
                KENYAN_PHONE,
                message="Enter a valid Kenyan mobile number."
            )
        ],
        render_kw={
            "maxlength": "10",
            "minlength": "10",
            "inputmode": "tel",
            "pattern": "(07|01)[0-9]{8}",
            "placeholder": "e.g. 0712345678"
        }
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[
            Optional(),
            Length(max=2000)
        ]
    )


# 1. New Building Plan Approval.
class NewBuildingPlanForm(BuildingPlanBaseForm):
    project_type = SelectField(
        "Type of Construction",
        choices=[
            ("residential", "Residential"),
            ("commercial", "Commercial"),
            ("industrial", "Industrial"),
            ("mixed_use", "Mixed Use"),
            ("institutional", "Institutional"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
        validate_choice=True
    )
    building_description = TextAreaField(
        "Description of Proposed Development",
        validators=[
            DataRequired(),
            Length(min=10, max=2000)
        ]
    )
    number_of_floors = IntegerField(
        "Number of Floors",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=100,
                        message="Enter a valid number of floors.")
        ]
    )
    estimated_project_value = IntegerField(
        "Estimated Project Value (KSh)",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=10000000000)
        ]
    )
    architect_name = StringField(
        "Architect's Name",
        validators=[
            DataRequired(),
            Length(min=2, max=150),
            Regexp(
                TEXT_WITH_LETTERS,
                message="Enter a valid architect's name."
            )
        ]
    )
    architect_registration = StringField(
        "Architect Registration Number",
        validators=[
            DataRequired(),
            Length(min=2, max=60),
            Regexp(REFERENCE_NUMBER,
                   message="Enter a valid registration number.")
        ]
    )
    
    submit = SubmitField("Submit Plan")


# 2. Revised Building Plans.
class RevisedBuildingPlanForm(BuildingPlanBaseForm):
    previous_approval_reference = StringField(
        "Previous Approval Reference",
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(REFERENCE_NUMBER,
                   message="Enter a valid approval reference.")
        ]
    )
    revision_details = TextAreaField(
        "Details of Proposed Changes",
        validators=[
            DataRequired(),
            Length(min=10, max=2000)
        ]
    )

    submit = SubmitField("Submit Changes")


# 3. Building Plan Resubmission.
class BuildingPlanResubmissionForm(BuildingPlanBaseForm):
    previous_application_reference = StringField(
        "Previous Application Reference",
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(REFERENCE_NUMBER,
                   message="Enter a valid application reference.")
        ]
    )
    corrections_made = TextAreaField(
        "Corrections and Changes Made",
        validators=[
            DataRequired(),
            Length(min=10, max=2000)
        ]
    )

    submit = SubmitField("Resubmit Plans")


# 4. Building Plan Extension.
class BuildingPlanExtensionForm(BuildingPlanBaseForm):
    previous_approval_reference = StringField(
        "Previous Approval Reference",
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(REFERENCE_NUMBER,
                   message="Enter a valid approval reference.")
        ]
    )
    approval_expiry_date = StringField(
        "Approval Expiry Date (YYYY-MM-DD)",
        validators=[
            DataRequired(),
            Regexp(
                r"^\d{4}-\d{2}-\d{2}$",
                message="Enter the date in YYYY-MM-DD format."
            )
        ],
        render_kw={
            "placeholder": "e.g. 2026-12-31"
        }
    )
    construction_status = SelectField(
        "Current Construction Status",
        choices=[
            ("not_started", "Construction Not Started"),
            ("ongoing", "Construction Ongoing"),
            ("suspended", "Construction Suspended"),
        ],
        validators=[DataRequired()],
        validate_choice=True
    )
    extension_reason = TextAreaField(
        "Reason for Extension Request",
        validators=[
            DataRequired(),
            Length(min=10, max=2000)
        ]
    )

    submit = SubmitField("Submit Request")

