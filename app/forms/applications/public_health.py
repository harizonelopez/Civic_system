from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp
)

KENYAN_PHONE = r"^(?:07|01)\d{8}$"
TEXT_WITH_LETTERS = r"^(?=.*[A-Za-z])[A-Za-zÀ-ÿ0-9\s&'().,/ -]+$"

class PublicHealthBaseForm(FlaskForm):
    contact_phone = StringField(
        "Contact Number",
        validators=[
            DataRequired(),
            Regexp(
                KENYAN_PHONE,
                message="Enter a valid Kenyan phone number."
            )
        ],
        render_kw={
            "placeholder": "e.g. 0712345678",
            "maxlength": "10",
            "inputmode": "numeric"
        }
    )
    premises_location = StringField(
        "Physical Location",
        validators=[
            DataRequired(),
            Length(max=180)
        ],
        render_kw={
            "placeholder": "Enter the physical location"
        }
    )
    ward = StringField(
        "Ward",
        validators=[
            DataRequired(),
            Length(max=100)
        ],
        render_kw={
            "placeholder": "Enter ward"
        }
    )


class FoodHygieneInspectionForm(PublicHealthBaseForm):
    premises_name = StringField(
        "Food Premises Name",
        validators=[
            DataRequired(),
            Length(max=180)
        ]
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
        validators=[
            Optional(),
            Length(max=50)
        ]
    )
    food_activities = TextAreaField(
        "Food Handling Activities",
        validators=[
            DataRequired(),
            Length(max=2000)
        ],
        render_kw={
            "rows": 4,
            "placeholder": "Describe the food preparation, handling or selling activities."
        }
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[
            Optional(),
            Length(max=2000)
        ]
    )

    submit = SubmitField("Submit Request")


class FoodHandlerCertificateForm(FlaskForm):
    full_name = StringField(
        "Applicant Full Name",
        validators=[
            DataRequired(),
            Length(max=150),
            Regexp(
                TEXT_WITH_LETTERS,
                message="Enter a valid full name."
            )
        ]
    )
    contact_phone = StringField(
        "Contact Number",
        validators=[
            DataRequired(),
            Regexp(
                KENYAN_PHONE,
                message="Enter a valid Kenyan phone number."
            )
        ],
        render_kw={
            "placeholder": "e.g. 0712345678",
            "maxlength": "10",
            "inputmode": "numeric"
        }
    )
    employer_name = StringField(
        "Employer or Food Premises Name",
        validators=[
            DataRequired(),
            Length(max=180)
        ]
    )
    premises_location = StringField(
        "Workplace Location",
        validators=[
            DataRequired(),
            Length(max=180)
        ]
    )
    ward = StringField(
        "Ward",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[
            Optional(),
            Length(max=2000)
        ]
    )

    submit = SubmitField("Submit Application")


class PublicHealthPremisesInspectionForm(PublicHealthBaseForm):
    applicant_name = StringField(
        "Applicant Full Name",
        validators=[
            DataRequired(),
            Length(max=150),
            Regexp(
                TEXT_WITH_LETTERS,
                message="Enter a valid full name."
            )
        ]
    )
    premises_name = StringField(
        "Premises Name",
        validators=[
            DataRequired(),
            Length(max=180)
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
            Length(max=2000)
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
            Length(max=2000)
        ]
    )

    submit = SubmitField("Submit Request")


class PublicHealthComplaintForm(FlaskForm):
    contact_phone = StringField(
        "Contact Number (Optional)",
        validators=[
            Optional(),
            Regexp(
                KENYAN_PHONE,
                message="Enter a valid Kenyan phone number."
            )
        ],
        render_kw={
            "placeholder": "e.g. 0712345678",
            "maxlength": "10",
            "inputmode": "numeric"
        }
    )
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
            Length(max=180)
        ]
    )
    ward = StringField(
        "Ward",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )
    date_observed = StringField(
        "Date Issue Was Observed",
        validators=[
            Optional(),
            Regexp(
                r"^\d{4}-\d{2}-\d{2}$",
                message="Enter the date in YYYY-MM-DD format."
            )
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
            "rows": 5,
            "placeholder": "Describe the public health concern and its impact."
        }
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[
            Optional(),
            Length(max=2000)
        ]
    )

    submit = SubmitField("Submit Complaint")

