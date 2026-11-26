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
    NumberRange,
    Regexp
)
from wtforms.fields import DateField

# Text fields containing letters, numbers and common punctuation.
TEXT_WITH_LETTERS = r"^(?=.*[A-Za-z])[A-Za-zÀ-ÿ0-9\s&'().,/ -]+$"

# Property and approval reference numbers.
REFERENCE_NUMBER = r"^[A-Za-z0-9/-]+$"

# Reusable property and contact information.
class BuildingPlanBaseForm(FlaskForm):
    property_location = StringField(
        "Property Location",
        validators=[
            DataRequired(),
            Length(min=3, max=150),
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
            Length(min=2, max=50),
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
            Length(min=2, max=20),
            Regexp(
                REFERENCE_NUMBER,
                message="Enter a valid plot or land reference number."
            )
        ]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )


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
            Length(min=10, max=500)
        ]
    )
    number_of_floors = IntegerField(
        "Number of Floors",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=100, message="Enter a valid number of floors.")
        ]
    )
    estimated_project_value = IntegerField(
        "Estimated Project Value (KSh)",
        validators=[
            DataRequired(),
            NumberRange(min=1000, max=10000000000)
        ]
    )
    architect_name = StringField(
        "Architect's Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
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
            Length(min=2, max=20),
            Regexp(REFERENCE_NUMBER,
                   message="Enter a valid registration number.")
        ]
    )
    
    submit = SubmitField("Submit Plan")


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
            Length(min=10, max=500)
        ]
    )

    submit = SubmitField("Submit Changes")


class BuildingPlanResubmissionForm(BuildingPlanBaseForm):
    previous_application_reference = StringField(
        "Previous Application Reference",
        validators=[
            DataRequired(),
            Length(min=3, max=20),
            Regexp(REFERENCE_NUMBER,
                   message="Enter a valid application reference.")
        ]
    )
    corrections_made = TextAreaField(
        "Corrections and Changes Made",
        validators=[
            DataRequired(),
            Length(min=10, max=500)
        ]
    )

    submit = SubmitField("Resubmit Plans")


class BuildingPlanExtensionForm(BuildingPlanBaseForm):
    previous_approval_reference = StringField(
        "Previous Approval Reference",
        validators=[
            DataRequired(),
            Length(min=3, max=20),
            Regexp(REFERENCE_NUMBER,
                   message="Enter a valid approval reference.")
        ]
    )
    approval_expiry_date = DateField(
        "Approval Expiry Date",
        format="%Y-%m-%d",
        validators=[DataRequired()],
        render_kw={"type": "date"}
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
            Length(min=10, max=500)
        ]
    )

    submit = SubmitField("Submit Request")

