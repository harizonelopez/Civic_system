from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    phone_number = db.Column(
        db.String(20),
        unique=True,
        nullable=True
    )

    gender = db.Column(
        db.String(10), 
        nullable=True
    )

    national_id = db.Column(
        db.String(8),
        unique=True,
        nullable=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=True
    )

    department = db.relationship(
        "Department",
        back_populates="users"
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    is_verified = db.Column(
        db.Boolean,
        default=False,
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

    last_login_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    roles = db.relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
        lazy="selectin"
    )

    service_requests = db.relationship(
        "ServiceRequest",
        back_populates="citizen",
        lazy="selectin"
    )

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_role(self, role_name):
        return any(
            role.name == role_name
            for role in self.roles
        )

    def has_permission(self, permission_code):
        return any(
            role.has_permission(permission_code)
            for role in self.roles
        )

    def __repr__(self):
        return f"<User {self.email}>"
