from datetime import datetime, timezone
from app.extensions import db

class ServiceCategory(db.Model):
    __tablename__ = "service_categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    description = db.Column(db.Text)

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

    services = db.relationship(
        "Service",
        back_populates="category",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<ServiceCategory {self.name}>"
