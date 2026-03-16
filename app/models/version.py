from app import db
from datetime import datetime

class DocumentVersion(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("document.id")
    )

    content = db.Column(db.Text)

    version_number = db.Column(db.Integer)

    created_by = db.Column(db.String(100))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )