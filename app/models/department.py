from datetime import datetime, timezone
from app.extensions import db

class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    code = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
        index=True
    )

    description = db.Column(db.Text)
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(10))
    location = db.Column(db.String(255))

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
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

    users = db.relationship(
        "User",
        back_populates="department",
        lazy="selectin"
    )

    services = db.relationship(
        "Service",
        back_populates="department",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Department {self.name}>"
