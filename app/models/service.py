from datetime import datetime, timezone
from decimal import Decimal
from app.extensions import db

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(180),
        nullable=False
    )

    code = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    description = db.Column(db.Text, nullable=False)

    requirements = db.Column(db.Text)

    processing_days = db.Column(
        db.Integer,
        nullable=True
    )

    fee = db.Column(
        db.Numeric(10, 2),
        default=Decimal("0.00"),
        nullable=False
    )

    is_online = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("service_categories.id"),
        nullable=True
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

    department = db.relationship(
        "Department",
        back_populates="services"
    )

    category = db.relationship(
        "ServiceCategory",
        back_populates="services"
    )

    service_requests = db.relationship(
        "ServiceRequest",
        back_populates="service",
        lazy="selectin"
    )

    service_options = db.relationship(
        "ServiceOption",
        back_populates="service",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Service {self.name}>"
