"""
forms.py - WTForms form definitions with validation
"""

import re
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    ValidationError,
)


# ── Custom validator ─────────────────────────────────────────────────────────
def validate_phone(form, field):
    """
    Accept common phone formats:
      +1-800-555-0199
      (800) 555-0199
      800.555.0199
      08001234567
    Must be 7-15 digits after stripping non-numeric characters.
    """
    digits = re.sub(r"\D", "", field.data)
    if len(digits) < 7 or len(digits) > 15:
        raise ValidationError(
            "Please enter a valid phone number (7–15 digits)."
        )


# ── Contact form ─────────────────────────────────────────────────────────────
class ContactForm(FlaskForm):
    """Main contact form rendered on the index page."""

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(message="Name is required."),
            Length(min=2, max=120, message="Name must be 2–120 characters."),
        ],
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address."),
            Length(max=254, message="Email must be 254 characters or fewer."),
        ],
    )

    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(message="Phone number is required."),
            validate_phone,
        ],
    )

    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Message is required."),
            Length(
                min=20,
                max=2000,
                message="Message must be between 20 and 2 000 characters.",
            ),
        ],
    )
