from datetime import datetime, timezone
from app.extensions import db

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    notification_type = db.Column(
        db.String(20),
        nullable=False,
        index=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    link = db.Column(
        db.String(255),
        nullable=True
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )

    user = db.relationship("User")

    def __repr__(self):
        return f"<Notification {self.id} for user {self.user_id}>"

