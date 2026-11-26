from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    IntegerField,
    SubmitField,
    ValidationError
)
from wtforms.validators import (
    DataRequired,
    Optional,
    Length,
    NumberRange,
)
from datetime import date
from wtforms.fields import DateField

# Reject future dates for incidents that have already occurred.
def validate_not_future_date(form, field):
    if field.data and field.data > date.today():
        raise ValidationError("Observed date can't be in the future.")

class FireSafetyInspectionForm(FlaskForm):
    premises_name = StringField(
        "Premises / Business Name",
        validators=[DataRequired(), Length(max=100)]
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
        validators=[DataRequired(), Length(max=100)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=50)]
    )
    number_of_floors = IntegerField(
        "Number of Floors",
        validators=[Optional(), NumberRange(min=1, max=100)]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=500)]
    )

    submit = SubmitField("Submit Request")


class FireSafetyCertificateForm(FlaskForm):
    premises_name = StringField(
        "Premises / Business Name",
        validators=[DataRequired(), Length(max=100)]
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
        validators=[DataRequired(), Length(max=100)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=50)]
    )
    previous_inspection_reference = StringField(
        "Previous Inspection Reference (if available)",
        validators=[Optional(), Length(max=100)]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=500)]
    )

    submit = SubmitField("Submit Request")


class FireSafetyReinspectionForm(FlaskForm):
    premises_name = StringField(
        "Premises / Business Name",
        validators=[DataRequired(), Length(max=100)]
    )
    premises_location = StringField(
        "Physical Location",
        validators=[DataRequired(), Length(max=100)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=50)]
    )
    previous_inspection_reference = StringField(
        "Previous Inspection Reference",
        validators=[DataRequired(), Length(max=100)]
    )
    corrective_actions = TextAreaField(
        "Corrective Actions Taken",
        validators=[DataRequired(), Length(max=500)]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=500)]
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
        validators=[DataRequired(), Length(max=100)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=50)]
    )
    description = TextAreaField(
        "Describe the Complaint",
        validators=[DataRequired(), Length(min=10, max=500)]
    )
    observed_date = DateField(
        "Date Observed",
        format="%Y-%m-%d",
        validators=[
            Optional(),
            validate_not_future_date
        ],
        render_kw={
            "type": "date"
        }
    )

    submit = SubmitField("Submit Complaint")

