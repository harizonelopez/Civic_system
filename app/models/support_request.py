import uuid
from datetime import datetime, timezone
from app.extensions import db


class SupportRequest(db.Model):
    __tablename__ = "support_requests"
    id = db.Column(db.Integer, primary_key=True)

    reference_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: f"SUP-{uuid.uuid4().hex[:12].upper()}"
    )

    # Citizen information
    citizen_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)

    # Support request information
    category = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(180), nullable=False)
    application_reference = db.Column(
        db.String(30),
        nullable=True,
        index=True
    )
    message = db.Column(db.Text, nullable=False)

    # Administration
    status = db.Column(
        db.String(30),
        default="submitted",
        nullable=False,
        index=True
    )

    admin_response = db.Column(db.Text, nullable=True)

    submitted_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    resolved_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    citizen = db.relationship("User")

    def __repr__(self):
        return f"<SupportRequest {self.reference_number}>"
    
