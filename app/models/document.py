from app import db
from datetime import datetime

class Document(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    versions = db.relationship(
        "DocumentVersion",
        backref="document",
        cascade="all, delete"
    )