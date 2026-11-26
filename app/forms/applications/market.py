from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField,
    ValidationError
)
from wtforms.validators import (
    DataRequired,
    Optional,
    Length
)
from datetime import date
from wtforms.fields import DateField

# Reject future dates for incidents that have already occurred.
def validate_not_future_date(form, field):
    if field.data and field.data > date.today():
        raise ValidationError("Incident date can't be in the future.")

class MarketStallApplicationForm(FlaskForm):
    business_name = StringField(
        "Business Name",
        validators=[DataRequired(), Length(max=100)]
    )
    business_type = SelectField(
        "Type of Business",
        choices=[
            ("", "Select business type"),
            ("retail", "Retail Shop"),
            ("food", "Food / Grocery Vendor"),
            ("clothing", "Clothing / Textile"),
            ("produce", "Agricultural Produce"),
            ("hardware", "Hardware / Building Materials"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    preferred_market = StringField(
        "Preferred Market",
        validators=[DataRequired(), Length(max=150)]
    )
    preferred_stall_type = SelectField(
        "Preferred Stall Type",
        choices=[
            ("", "Select stall type"),
            ("open_stall", "Open Stall"),
            ("lockable_stall", "Lockable Stall"),
            ("shop", "Market Shop"),
            ("kiosk", "Kiosk"),
        ],
        validators=[DataRequired()]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=60)]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=500)]
    )

    submit = SubmitField("Submit Application")


class MarketStallRenewalForm(FlaskForm):
    business_name = StringField(
        "Business Name",
        validators=[DataRequired(), Length(max=150)]
    )
    market_name = StringField(
        "Market Name",
        validators=[DataRequired(), Length(max=150)]
    )
    stall_number = StringField(
        "Current Stall Number",
        validators=[DataRequired(), Length(max=50)]
    )
    allocation_reference = StringField(
        "Stall Allocation Reference",
        validators=[Optional(), Length(max=100)]
    )
    additional_information = TextAreaField(
        "Additional Information",
        validators=[Optional(), Length(max=500)]
    )

    submit = SubmitField("Submit Request")


class MarketStallTransferForm(FlaskForm):
    current_holder_name = StringField(
        "Current Stall Holder's Full Name",
        validators=[DataRequired(), Length(max=100)]
    )
    proposed_holder_name = StringField(
        "Proposed New Holder's Full Name",
        validators=[DataRequired(), Length(max=100)]
    )
    market_name = StringField(
        "Market Name",
        validators=[DataRequired(), Length(max=100)]
    )
    stall_number = StringField(
        "Stall Number",
        validators=[DataRequired(), Length(max=20)]
    )
    transfer_reason = TextAreaField(
        "Reason for Transfer",
        validators=[DataRequired(), Length(min=10, max=500)]
    )

    submit = SubmitField("Submit Request")


class MarketFacilityMaintenanceForm(FlaskForm):
    market_name = StringField(
        "Market Name",
        validators=[DataRequired(), Length(max=100)]
    )
    facility_type = SelectField(
        "Type of Facility",
        choices=[
            ("", "Select facility type"),
            ("stall", "Market Stall"),
            ("roof", "Roofing"),
            ("floor", "Flooring"),
            ("water", "Water Supply"),
            ("electricity", "Electrical Installation"),
            ("toilets", "Public Toilets"),
            ("drainage", "Drainage System"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    affected_location = StringField(
        "Specific Location of the Problem",
        validators=[DataRequired(), Length(max=50)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=50)]
    )
    problem_description = TextAreaField(
        "Describe the Maintenance Problem",
        validators=[DataRequired(), Length(min=10, max=500)]
    )

    submit = SubmitField("Submit Request")


class MarketSanitationForm(FlaskForm):
    market_name = StringField(
        "Market Name",
        validators=[DataRequired(), Length(max=100)]
    )
    sanitation_issue = SelectField(
        "Type of Sanitation Issue",
        choices=[
            ("", "Select sanitation issue"),
            ("waste_accumulation", "Accumulated Waste"),
            ("blocked_drainage", "Blocked Drainage"),
            ("dirty_toilets", "Dirty Public Toilets"),
            ("stagnant_water", "Stagnant Water"),
            ("pest_infestation", "Pest Infestation"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    affected_location = StringField(
        "Affected Location",
        validators=[DataRequired(), Length(max=100)]
    )
    description = TextAreaField(
        "Describe the Sanitation Issue",
        validators=[DataRequired(), Length(min=10, max=500)]
    )

    submit = SubmitField("Submit Request")


class MarketComplaintForm(FlaskForm):
    complaint_category = SelectField(
        "Complaint Category",
        choices=[
            ("", "Select complaint category"),
            ("stall_allocation", "Unfair Stall Allocation"),
            ("market_fees", "Market Fees / Charges"),
            ("poor_services", "Poor Service Delivery"),
            ("trader_conduct", "Trader Misconduct"),
            ("facility_condition", "Poor Market Facility Conditions"),
            ("staff_conduct", "Staff Misconduct"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )
    market_name = StringField(
        "Market Name",
        validators=[DataRequired(), Length(max=100)]
    )
    affected_location = StringField(
        "Location of Concern (if applicable)",
        validators=[Optional(), Length(max=100)]
    )
    description = TextAreaField(
        "Describe the Complaint",
        validators=[DataRequired(), Length(min=10, max=500)]
    )
    observed_date = DateField(
        "Date of Incident",
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

