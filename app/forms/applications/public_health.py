from flask_wtf import FlaskForm
from datetime import date
from wtforms.fields import DateField
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField,
    ValidationError
)
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp
)

TEXT_WITH_LETTERS = r"^(?=.*[A-Za-z])[A-Za-zÀ-ÿ0-9\s&'().,/ -]+$"

# Reject future dates for incidents that have already occurred.
def validate_not_future_date(form, field):
    if field.data and field.data > date.today():
        raise ValidationError("Observed date can't be in the future.")
    

class PublicHealthBaseForm(FlaskForm):
    premises_location = StringField(
        "Physical Location",
        validators=[DataRequired(), Length(max=100)],
        render_kw={"placeholder": "Enter the physical location"}
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=50)],
        render_kw={"placeholder": "Enter ward"}
    )


class FoodHygieneInspectionForm(PublicHealthBaseForm):
    premises_name = StringField(
        "Food Premises Name",
        validators=[DataRequired(), Length(max=100)]
    )
    premises_type = SelectField(
        "Type of Food Premises",
        choices=[
            ("", "Select premises type"),
            ("retail_shop", "Retail Shop"),
            ("canteen", "Canteen"),
            ("eating_house", "Eating House"),
            ("restaurant", "Restaurant"),
            ("hotel", "Hotel"),
            ("other", "Other")
        ],
        validators=[DataRequired()],
        validate_choice=True
    )
    business_permit = StringField(
        "Business Permit Number",
        validators=[Optional(), Length(max=20)]
    )
    food_activities = TextAreaField(
        "Food Handling Activities",
        validators=[DataRequired(), Length(max=500)],
        render_kw={"rows": 4, "placeholder": "Describe the food preparation, handling or selling activities."}
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=500)]
    )

    submit = SubmitField("Submit Request")


class FoodHandlerCertificateForm(FlaskForm):
    full_name = StringField(
        "Applicant Full Name",
        validators=[
            DataRequired(),
            Length(max=100),
            Regexp(
                TEXT_WITH_LETTERS,
                message="Enter a valid full name."
            )
        ]
    )
    employer_name = StringField(
        "Employer or Food Premises Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )
    premises_location = StringField(
        "Workplace Location",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )
    ward = StringField(
        "Ward",
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )

    submit = SubmitField("Submit Application")


class PublicHealthPremisesInspectionForm(PublicHealthBaseForm):
    premises_name = StringField(
        "Premises Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )
    premises_type = SelectField(
        "Type of Premises",
        choices=[
            ("", "Select premises type"),
            ("business", "Business Premises"),
            ("residential", "Residential Premises"),
            ("institution", "Institution"),
            ("commercial", "Commercial Premises"),
            ("other", "Other")
        ],
        validators=[DataRequired()],
        validate_choice=True
    )
    inspection_reason = TextAreaField(
        "Reason for Inspection",
        validators=[
            DataRequired(),
            Length(max=500)
        ],
        render_kw={
            "rows": 4,
            "placeholder": "Explain why the premises requires inspection."
        }
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )

    submit = SubmitField("Submit Request")


class PublicHealthComplaintForm(FlaskForm):
    complaint_category = SelectField(
        "Complaint Category",
        choices=[
            ("", "Select complaint category"),
            ("poor_sanitation", "Poor Sanitation"),
            ("unsafe_food_handling", "Unsafe Food Handling"),
            ("improper_waste_disposal", "Improper Waste Disposal"),
            ("water_pollution", "Water Pollution"),
            ("public_nuisance", "Public Nuisance"),
            ("other", "Other")
        ],
        validators=[DataRequired()],
        validate_choice=True
    )
    affected_location = StringField(
        "Location of the Concern",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )
    ward = StringField(
        "Ward",
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    date_observed = DateField(
        "Date Issue Was Observed",
        format="%Y-%m-%d",
        validators=[
            Optional(),
            validate_not_future_date
        ],
        render_kw={
            "type": "date"
        }
    )
    complaint_description = TextAreaField(
        "Complaint Description",
        validators=[
            DataRequired(),
            Length(max=2000)
        ],
        render_kw={
            "rows": 4,
            "placeholder": "Describe the public health concern and its impact."
        }
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )

    submit = SubmitField("Submit Complaint")

