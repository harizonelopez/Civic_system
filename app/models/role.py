from app.extensions import db

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(
        db.Integer, 
        primary_key=True
    )

    name = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    users = db.relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )

    permissions = db.relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles",
        lazy="selectin"
    )

    def has_permission(self, permission_code):
        return any(
            permission.code == permission_code
            for permission in self.permissions
        )

    def __repr__(self):
        return f"<Role {self.name}>"
