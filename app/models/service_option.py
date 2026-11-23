from datetime import datetime, timezone
from decimal import Decimal
from app.extensions import db

class ServiceOption(db.Model):
    __tablename__ = "service_options"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    code = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    requirements = db.Column(
        db.Text,
    )

    eligibility = db.Column(
        db.Text,
        nullable=True
    )

    processing_days = db.Column(
        db.Integer,
        nullable=True
    )

    fee = db.Column(
        db.Numeric(10, 2),
        default=Decimal("0.00"),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id"),
        nullable=False,
        index=True
    )

    created_at = db.Column(
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

    service = db.relationship(
        "Service",
        back_populates="service_options"
    )

    service_requests = db.relationship(
        "ServiceRequest",
        back_populates="service_option",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<ServiceOption {self.name}>"
