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


class FireSafetyInspectionForm(FlaskForm):
    premises_name = StringField(
        "Premises / Business Name",
        validators=[DataRequired(), Length(max=150)]
    )
    premises_type = SelectField(
        "Type of Premises",
        choices=[
            ("", "Select premises type"),
            ("shop", "Shop / Retail Premises"),
            ("office", "Office"),
            ("restaurant", "Restaurant"),
            ("hotel", "Hotel / Accommodation"),
            ("industrial", "Industrial Premises"),
            ("public_building", "Public Building"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    premises_location = StringField(
        "Physical Location",
        validators=[DataRequired(), Length(max=200)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=100)]
    )
    number_of_floors = IntegerField(
        "Number of Floors",
        validators=[Optional(), NumberRange(min=1, max=200)]
    )
    contact_phone = StringField(
        "Contact Phone Number",
        validators=[
            DataRequired(),
            Regexp(
                r"^(?:07|01)\d{8}$",
                message="Enter a valid KE phone number."
            )
        ]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=1000)]
    )

    submit = SubmitField("Submit Request")


class FireSafetyCertificateForm(FlaskForm):
    premises_name = StringField(
        "Premises / Business Name",
        validators=[DataRequired(), Length(max=150)]
    )
    premises_type = SelectField(
        "Type of Premises",
        choices=[
            ("", "Select premises type"),
            ("shop", "Shop / Retail Premises"),
            ("office", "Office"),
            ("restaurant", "Restaurant"),
            ("hotel", "Hotel / Accommodation"),
            ("industrial", "Industrial Premises"),
            ("public_building", "Public Building"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    premises_location = StringField(
        "Physical Location",
        validators=[DataRequired(), Length(max=200)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=100)]
    )
    previous_inspection_reference = StringField(
        "Previous Inspection Reference (if available)",
        validators=[Optional(), Length(max=100)]
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


class FireSafetyReinspectionForm(FlaskForm):
    premises_name = StringField(
        "Premises / Business Name",
        validators=[DataRequired(), Length(max=150)]
    )
    premises_location = StringField(
        "Physical Location",
        validators=[DataRequired(), Length(max=200)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=100)]
    )
    previous_inspection_reference = StringField(
        "Previous Inspection Reference",
        validators=[DataRequired(), Length(max=100)]
    )
    corrective_actions = TextAreaField(
        "Corrective Actions Taken",
        validators=[DataRequired(), Length(max=2000)]
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


class FireSafetyComplaintForm(FlaskForm):
    complaint_category = SelectField(
        "Complaint Category",
        choices=[
            ("", "Select complaint category"),
            ("blocked_exit", "Blocked Emergency Exit"),
            ("faulty_equipment", "Faulty Firefighting Equipment"),
            ("unsafe_storage", "Unsafe Storage of Flammable Materials"),
            ("electrical_hazard", "Electrical Fire Hazard"),
            ("fire_hazard", "General Fire Hazard"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    affected_location = StringField(
        "Location of Fire Safety Concern",
        validators=[DataRequired(), Length(max=200)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=100)]
    )
    description = TextAreaField(
        "Describe the Complaint",
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

    submit = SubmitField("Submit Complaint")

