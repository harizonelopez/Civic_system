from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional
)


class SupportRequestForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(max=255)
        ]
    )

    category = SelectField(
        "What do you need help with?",
        choices=[
            ("application", "Application Issues"),
            ("account", "Account & Login Issues"),
            ("service", "Public Service Enquiries"),
            ("technical", "Technical Problems"),
            ("other", "Other"),
        ],
        validators=[DataRequired()]
    )

    subject = StringField(
        "Subject",
        validators=[
            DataRequired(),
            Length(min=5, max=180)
        ]
    )

    application_reference = StringField(
        "Application Reference (Optional)",
        validators=[
            Optional(),
            Length(max=30)
        ]
    )

    message = TextAreaField(
        "Describe Your Problem",
        validators=[
            DataRequired(),
            Length(min=20, max=3000)
        ]
    )

    submit = SubmitField("Submit Support Request")
