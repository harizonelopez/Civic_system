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

class MarketStallApplicationForm(FlaskForm):
    applicant_name = StringField(
        "Applicant Full Name",
        validators=[DataRequired(), Length(max=150)]
    )
    national_id = StringField(
        "National ID Number",
        validators=[DataRequired(), Length(min=6, max=20)]
    )
    business_name = StringField(
        "Business Name",
        validators=[DataRequired(), Length(max=150)]
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

    submit = SubmitField("Submit Application")


class MarketStallRenewalForm(FlaskForm):
    applicant_name = StringField(
        "Applicant Full Name",
        validators=[DataRequired(), Length(max=150)]
    )
    national_id = StringField(
        "National ID Number",
        validators=[DataRequired(), Length(min=6, max=20)]
    )
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


class MarketStallTransferForm(FlaskForm):
    current_holder_name = StringField(
        "Current Stall Holder's Full Name",
        validators=[DataRequired(), Length(max=150)]
    )
    national_id = StringField(
        "Current Holder's National ID Number",
        validators=[DataRequired(), Length(min=6, max=20)]
    )
    proposed_holder_name = StringField(
        "Proposed New Holder's Full Name",
        validators=[DataRequired(), Length(max=150)]
    )
    proposed_holder_id = StringField(
        "Proposed Holder's National ID Number",
        validators=[DataRequired(), Length(min=6, max=20)]
    )
    market_name = StringField(
        "Market Name",
        validators=[DataRequired(), Length(max=150)]
    )
    stall_number = StringField(
        "Stall Number",
        validators=[DataRequired(), Length(max=50)]
    )
    transfer_reason = TextAreaField(
        "Reason for Transfer",
        validators=[DataRequired(), Length(min=10, max=1000)]
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

    submit = SubmitField("Submit Request")


class MarketFacilityMaintenanceForm(FlaskForm):
    applicant_name = StringField(
        "Applicant Full Name",
        validators=[DataRequired(), Length(max=150)]
    )
    market_name = StringField(
        "Market Name",
        validators=[DataRequired(), Length(max=150)]
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
        validators=[DataRequired(), Length(max=200)]
    )
    ward = StringField(
        "Ward",
        validators=[DataRequired(), Length(max=100)]
    )
    problem_description = TextAreaField(
        "Describe the Maintenance Problem",
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

    submit = SubmitField("Submit Request")


class MarketSanitationForm(FlaskForm):
    applicant_name = StringField(
        "Applicant Full Name",
        validators=[DataRequired(), Length(max=150)]
    )
    market_name = StringField(
        "Market Name",
        validators=[DataRequired(), Length(max=150)]
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
        validators=[DataRequired(), Length(max=200)]
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
        validators=[DataRequired(), Length(max=150)]
    )
    affected_location = StringField(
        "Location of Concern (if applicable)",
        validators=[Optional(), Length(max=200)]
    )
    description = TextAreaField(
        "Describe the Complaint",
        validators=[DataRequired(), Length(min=10, max=2000)]
    )
    observed_date = StringField(
        "Date of Incident (e.g. 24/11/2026)",
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

