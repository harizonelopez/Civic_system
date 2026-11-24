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
    Optional,
    Length,
    Regexp,
    NumberRange,
)

class HouseholdWasteCollectionForm(FlaskForm):
    property_type = SelectField(
        "Type of Property",
        choices=[
            ("", "Select property type"),
            ("residential", "Residential House"),
            ("apartment", "Apartment / Flats"),
            ("estate", "Residential Estate"),
            ("institution", "Institution"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    property_location = StringField(
        "Physical Location",
        validators=[DataRequired(), Length(max=200)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=100)]
    )
    number_of_households = IntegerField(
        "Number of Households",
        validators=[Optional(), NumberRange(min=1, max=10000)]
    )
    collection_frequency = SelectField(
        "Preferred Collection Frequency",
        choices=[
            ("", "Select collection frequency"),
            ("weekly", "Weekly"),
            ("twice_weekly", "Twice a Week"),
            ("monthly", "Monthly"),
        ],
        validators=[DataRequired()]
    )
    contact_phone = StringField(
        "Contact Phone Number",
        validators=[
            DataRequired(),
            Regexp(
                r"^(?:07|01)\d{8}$",
                message="Enter a valid Kenyan phone number."
            )
        ]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=1000)]
    )

    submit = SubmitField("Submit Request")


class CommercialWasteCollectionForm(FlaskForm):
    business_name = StringField(
        "Business / Organization Name",
        validators=[DataRequired(), Length(max=150)]
    )
    business_type = SelectField(
        "Type of Business",
        choices=[
            ("", "Select business type"),
            ("retail", "Retail Shop"),
            ("restaurant", "Restaurant / Hotel"),
            ("office", "Office"),
            ("market", "Market Business"),
            ("industrial", "Industrial Premises"),
            ("institution", "Institution"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    business_location = StringField(
        "Physical Business Location",
        validators=[DataRequired(), Length(max=200)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=100)]
    )
    estimated_waste_volume = SelectField(
        "Estimated Waste Volume",
        choices=[
            ("", "Select estimated waste volume"),
            ("small", "Small - Less than 50 kg per week"),
            ("medium", "Medium - 50 to 200 kg per week"),
            ("large", "Large - 200 to 500 kg per week"),
            ("very_large", "Very Large - Above 500 kg per week"),
        ],
        validators=[DataRequired()]
    )
    collection_frequency = SelectField(
        "Preferred Collection Frequency",
        choices=[
            ("", "Select collection frequency"),
            ("weekly", "Weekly"),
            ("twice_weekly", "Twice a Week"),
            ("daily", "Daily"),
        ],
        validators=[DataRequired()]
    )
    contact_phone = StringField(
        "Contact Phone Number",
        validators=[
            DataRequired(),
            Regexp(
                r"^(?:07|01)\d{8}$",
                message="Enter a valid Kenyan phone number."
            )
        ]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=1000)]
    )

    submit = SubmitField("Submit Request")


class BulkWasteCollectionForm(FlaskForm):
    applicant_name = StringField(
        "Applicant / Organization Name",
        validators=[DataRequired(), Length(max=150)]
    )
    waste_type = SelectField(
        "Type of Waste",
        choices=[
            ("", "Select waste type"),
            ("household", "Household Waste"),
            ("construction", "Construction Waste"),
            ("garden", "Garden / Green Waste"),
            ("furniture", "Furniture / Bulky Items"),
            ("commercial", "Commercial Waste"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    estimated_quantity = IntegerField(
        "Estimated Quantity (in bags or items)",
        validators=[DataRequired(), NumberRange(min=1, max=100000)]
    )
    collection_location = StringField(
        "Collection Location",
        validators=[DataRequired(), Length(max=200)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=100)]
    )
    contact_phone = StringField(
        "Contact Phone Number",
        validators=[
            DataRequired(),
            Regexp(
                r"^(?:07|01)\d{8}$",
                message="Enter a valid Kenyan phone number."
            )
        ]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=1000)]
    )

    submit = SubmitField("Submit Request")


class IllegalDumpingReportForm(FlaskForm):
    dumping_type = SelectField(
        "Type of Dumping",
        choices=[
            ("", "Select dumping type"),
            ("household", "Household Waste"),
            ("construction", "Construction Debris"),
            ("industrial", "Industrial Waste"),
            ("hazardous", "Hazardous Waste"),
            ("sewage", "Sewage / Wastewater"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    affected_location = StringField(
        "Location of Illegal Dumping",
        validators=[DataRequired(), Length(max=200)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=100)]
    )
    description = TextAreaField(
        "Describe the Illegal Dumping",
        validators=[DataRequired(), Length(min=10, max=2000)]
    )
    observed_date = StringField(
        "Date Observed (e.g. 24/11/2026)",
        validators=[Optional(), Length(max=20)]
    )
    contact_phone = StringField(
        "Contact Phone Number (optional)",
        validators=[
            Optional(),
            Regexp(
                r"^(?:07|01)\d{8}$",
                message="Enter a valid Kenyan phone number."
            )
        ]
    )

    submit = SubmitField("Submit Report")


class EnvironmentalSanitationRequestForm(FlaskForm):
    request_category = SelectField(
        "Sanitation Request Category",
        choices=[
            ("", "Select request category"),
            ("drainage", "Blocked Drainage"),
            ("sewage", "Sewage Problem"),
            ("public_cleaning", "Public Area Cleaning"),
            ("waste_accumulation", "Accumulated Waste"),
            ("stagnant_water", "Stagnant Water"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    affected_location = StringField(
        "Affected Location",
        validators=[DataRequired(), Length(max=200)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=100)]
    )
    description = TextAreaField(
        "Describe the Sanitation Issue",
        validators=[DataRequired(), Length(min=10, max=2000)]
    )
    contact_phone = StringField(
        "Contact Phone Number",
        validators=[
            DataRequired(),
            Regexp(
                r"^(?:07|01)\d{8}$",
                message="Enter a valid Kenyan phone number."
            )
        ]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=1000)]
    )

    submit = SubmitField("Submit Request")

