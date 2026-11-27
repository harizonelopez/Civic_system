from datetime import datetime, timezone
from app.extensions import db

class ApplicationRemark(db.Model):
    __tablename__ = "application_remarks"
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    remark = db.Column(
        db.Text, 
        nullable=False
    )
    application_id = db.Column(
        db.Integer,
        db.ForeignKey("service_requests.id"),
        nullable=False,
        index=True
    )
    admin_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    application = db.relationship(
        "ServiceRequest",
        back_populates="remarks"
    )
    admin = db.relationship(
        "User",
        back_populates="application_remarks"
    )


    def __repr__(self):
        return f"<ApplicationRemark {self.id}>"
