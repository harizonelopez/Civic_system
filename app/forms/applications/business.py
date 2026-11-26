from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
)

# Text fields must contain letters, numbers and common punctuation where appropriate.
TEXT_WITH_LETTERS = r"^(?=.*[A-Za-z])[A-Za-zÀ-ÿ0-9\s&'().,/ -]+$"

# Permit numbers may contain letters, digits, hyphens and slashes.
PERMIT_NUMBER = r"^[A-Za-z0-9/-]+$"

class NewBusinessPermitForm(FlaskForm):
    business_name = StringField(
        "Business Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
            Regexp(
                TEXT_WITH_LETTERS,
                message="Enter a valid business name."
            )
        ]
    )
    business_type = SelectField(
        "Business Type",
        choices=[
            ("sole_proprietorship", "Sole Proprietorship"),
            ("partnership", "Partnership"),
            ("limited_company", "Limited Company"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
        validate_choice=True
    )
    business_activity = StringField(
        "Nature of Business",
        validators=[
            DataRequired(),
            Length(min=3, max=150),
            Regexp(
                TEXT_WITH_LETTERS,
                message="Enter a valid business activity."
            )
        ]
    )
    business_location = StringField(
        "Business Location",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
            Regexp(
                TEXT_WITH_LETTERS,
                message="Enter a valid business location."
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
    postal_address = StringField(
        "Postal Address",
        validators=[
            Optional(),
            Length(max=150),
            Regexp(
                r"^[A-Za-z0-9\s,./-]+$",
                message="Enter a valid postal address."
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

    submit = SubmitField("Submit Application")


class RenewBusinessPermitForm(FlaskForm):
    permit_number = StringField(
        "Existing Permit Number",
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                PERMIT_NUMBER,
                message="Permit number can only contain letters, numbers, hyphens and slashes."
            )
        ]
    )
    business_name = StringField(
        "Business Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
            Regexp(TEXT_WITH_LETTERS,
                   message="Enter a valid business name.")
        ]
    )
    business_location = StringField(
        "Business Location",
        validators=[
            DataRequired(),
            Length(min=2, max=150),
            Regexp(TEXT_WITH_LETTERS,
                   message="Enter a valid business location.")
        ]
    )
    ward = StringField(
        "Ward",
        validators=[
            DataRequired(),
            Length(min=2, max=50),
            Regexp(TEXT_WITH_LETTERS,
                   message="Enter a valid ward name.")
        ]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )

    submit = SubmitField("Submit Renewal")


class AmendBusinessPermitForm(FlaskForm):
    permit_number = StringField(
        "Existing Permit Number",
        validators=[
            DataRequired(),
            Length(min=3, max=20),
            Regexp(
                PERMIT_NUMBER,
                message="Permit number can only contain letters, numbers, hyphens and slashes."
            )
        ]
    )
    amendment_type = SelectField(
        "Type of Amendment",
        choices=[
            ("business_name", "Change of Business Name"),
            ("business_location", "Change of Business Location"),
            ("business_activity", "Change of Business Activity"),
            ("ownership", "Change of Ownership"),
            ("other", "Other"),
        ],
        validators=[DataRequired()],
        validate_choice=True
    )
    amendment_details = TextAreaField(
        "Amendment Details",
        validators=[
            DataRequired(),
            Length(min=10, max=500),
            Regexp(
                TEXT_WITH_LETTERS,
                message="Please provide meaningful amendment details."
            )
        ]
    )

    submit = SubmitField("Submit Amendment")
