"""
models.py - SQLAlchemy database models
"""

from datetime import datetime, timezone
from app import db


class ContactSubmission(db.Model):
    """Stores every validated contact-form submission."""

    __tablename__ = "contact_submissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    message = db.Column(db.Text, nullable=False)
    # Auto-stamped in UTC at insert time
    submitted_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    # Store the client IP for basic audit logging
    ip_address = db.Column(db.String(45), nullable=True)

    def __repr__(self):
        return f"<ContactSubmission id={self.id} email={self.email!r}>"

    def to_dict(self):
        """Serialize to plain dict (useful for JSON responses / logging)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "message": self.message,
            "submitted_at": self.submitted_at.isoformat(),
            "ip_address": self.ip_address,
        }
