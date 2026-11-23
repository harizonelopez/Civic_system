import uuid
from datetime import datetime, timezone
from app.extensions import db

class ServiceRequest(db.Model):
    __tablename__ = "service_requests"
    id = db.Column(db.Integer, primary_key=True)
    
    reference_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: f"CSR-{uuid.uuid4().hex[:12].upper()}"
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    # Featured service identification
    service_slug = db.Column(
        db.String(80),
        nullable=True,
        index=True
    )

    option_code = db.Column(
        db.String(80),
        nullable=True
    )

    # Stores service specific application form data
    form_data = db.Column(
        db.JSON,
        nullable=False,
        default=dict
    )

    # Preserves service info at submission time
    service_snapshot = db.Column(
        db.JSON,
        nullable=False,
        default = dict
    )

    status = db.Column(
        db.String(30),
        default="submitted",
        nullable=False,
        index=True
    )

    priority = db.Column(
        db.String(20),
        default="normal",
        nullable=False
    )

    citizen_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id"),
        nullable=True,
        index=True
    )

    service_option_id = db.Column(
        db.Integer,
        db.ForeignKey("service_options.id"),
        nullable=True,
        index=True
    )

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

    closed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    citizen = db.relationship(
        "User",
        back_populates="service_requests"
    )

    service = db.relationship(
        "Service",
        back_populates="service_requests"
    )

    service_option = db.relationship(
        "ServiceOption",
        back_populates="service_requests"
    )

    def __repr__(self):
        return f"<ServiceRequest {self.reference_number}>"
