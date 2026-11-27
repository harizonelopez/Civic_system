from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    Regexp,
    ValidationError,
)
from difflib import get_close_matches

COMMON_EMAIL_DOMAINS = [
    "gmail.com",
    "outlook.com",
    "hotmail.com",
    "yahoo.com",
    "icloud.com",
    "live.com",
    "protonmail.com",
]

def validate_email_domain(form, field):
    domain = field.data.rsplit("@", 1)[-1].lower()

    if domain in COMMON_EMAIL_DOMAINS:
        return 
    
    suggestions = get_close_matches(
        domain,
        COMMON_EMAIL_DOMAINS,
        n=1,
        cutoff=0.82
    )

    if suggestions:
        raise ValidationError(f"Did you mean {suggestions[0]}? Please check your email address.")

class RegistrationForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(max=50),
        ],
    )
    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Length(max=50),
        ],
    )
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(message="Enter a valid email address"),
            Length(max=100),
            validate_email_domain,
        ],
    )
    phone_number = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=10, max=10),
            Regexp(
                r"^(07|01)\d{8}$",
                message="Enter a valid KE phone number starting with 07 or 01.",
            ),
        ],
    )
    national_id = StringField(
        "National ID Number",
        validators=[
            DataRequired(),
            Length(min=8, max=8),
            Regexp(
                r"^[0-9]{8}$",
                message="National ID must contain exactly 8 digits."
            ),
        ],
        render_kw={
            "maxlength": "8",
            "minlength": "8",
            "inputmode": "numeric",
            "pattern": "[0-9]{8}",
            "placeholder": "Enter your 8-digit National ID",
        },
    )
    gender = SelectField(
        "Gender",
        choices=[
            ("", "Select Gender"),
            ("Male", "Male"),
            ("Female", "Female"),
        ],
        validators=[DataRequired(message="Select your gender")],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=128),
            Regexp(
                r"^(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).+$",
                message=("Password must contain a letter, a number & a special character "),
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )
    remember_me = BooleanField("Remember Me")

    submit = SubmitField("Sign In")


class ProfileForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(max=50),
        ],
    )
    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Length(max=50),
        ],
    )
    phone_number = StringField(
        "Phone Number",
        validators=[
            Optional(),
            Length(min=10, max=10),
            Regexp(
                r"^(07|01)\d{8}$",
                message="Enter a valid KE phone number starting with 07 or 01.",
            ),
        ],
    )
    national_id = StringField(
        "National ID Number",
        validators=[
            DataRequired(),
            Length(min=8, max=8),
            Regexp(
                r"^[0-9]{8}$",
                message="National ID must contain exactly 8 digits."
            ),
        ],
        render_kw={
            "maxlength": "8",
            "minlength": "8",
            "inputmode": "numeric",
            "pattern": "[0-9]{8}",
            "placeholder": "Enter your 8-digit National ID",
        },
    )
    gender = SelectField(
        "Gender",
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ],
        validators=[DataRequired(message="Select your gender")],
    )

    submit = SubmitField("Save Changes")


class AdminCitizenForm(ProfileForm):
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(max=100)
        ]
    )


class PasswordResetVerificationForm(FlaskForm):
    email = StringField(
        "Registered Email Address",
        validators=[
            DataRequired(),
            Email(message="Enter a valid email address."),
            Length(max=100),
        ],
    )
    national_id = StringField(
        "National ID Number",
        validators=[
            DataRequired(),
            Length(min=8, max=8),
            Regexp(
                r"^[0-9]{8}$",
                message="National ID must contain exactly 8 digits.",
            ),
        ],
        render_kw={
            "maxlength": "8",
            "minlength": "8",
            "inputmode": "numeric",
            "pattern": "[0-9]{8}",
            "placeholder": "Enter your 8-digit National ID",
        },
    )

    submit = SubmitField("Verify Identity")


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8, max=128),
            Regexp(
                r"^(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).+$",
                message="Password must contain a letter, a number and a special character.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords dodn't match."),
        ],
    )

    submit = SubmitField("Reset Password")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current Password",
        validators=[
            DataRequired(message="Enter your current password."),
        ],
    )
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8, max=128),
            Regexp(
                r"^(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).+$",
                message="Password must contain a letter, a number and a special character.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("new_password", message="Passwords must match."),
        ],
    )

    change_password = SubmitField("Update Password")
