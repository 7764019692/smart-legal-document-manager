from flask import Blueprint, request, jsonify
from app import db
from app.models.document import Document
from app.models.version import DocumentVersion
from app.services.diff_service import compare_text
from app.services.notification_service import is_significant_change, notify_async

document_bp = Blueprint("document", __name__)


@document_bp.route("/")
def home():
    return {"message": "Smart Legal Document Manager API running"}


# CREATE DOCUMENT
@document_bp.route("/documents", methods=["POST"])
def create_document():

    data = request.json

    title = data["title"]
    text = data["text"]
    user = data.get("user", "unknown")

    document = Document(title=title)
    db.session.add(document)
    db.session.commit()

    version = DocumentVersion(
        document_id=document.id,
        content=text,
        version_number=1,
        created_by=user
    )

    db.session.add(version)
    db.session.commit()

    return jsonify({
        "message": "Document created",
        "document_id": document.id
    })


# CREATE NEW VERSION
@document_bp.route("/documents/<int:doc_id>/version", methods=["POST"])
def create_version(doc_id):

    data = request.json
    text = data["text"]
    user = data.get("user", "unknown")

    latest = DocumentVersion.query.filter_by(
        document_id=doc_id
    ).order_by(
        DocumentVersion.version_number.desc()
    ).first()

    new_version = DocumentVersion(
        document_id=doc_id,
        content=text,
        version_number=latest.version_number + 1,
        created_by=user
    )

    db.session.add(new_version)
    db.session.commit()

    if is_significant_change(latest.content, text):
        notify_async(doc_id)

    return jsonify({"message": "New version created"})


# COMPARE VERSIONS
@document_bp.route("/documents/<int:doc_id>/compare")
def compare_versions(doc_id):

    v1 = int(request.args.get("v1"))
    v2 = int(request.args.get("v2"))

    version1 = DocumentVersion.query.filter_by(
        document_id=doc_id,
        version_number=v1
    ).first()

    version2 = DocumentVersion.query.filter_by(
        document_id=doc_id,
        version_number=v2
    ).first()

    diff = compare_text(
        version1.content,
        version2.content
    )

    return jsonify({"difference": diff})


# UPDATE DOCUMENT TITLE
@document_bp.route("/documents/<int:doc_id>/title", methods=["PATCH"])
def update_title(doc_id):

    data = request.json

    doc = Document.query.get(doc_id)

    doc.title = data["title"]

    db.session.commit()

    return jsonify({"message": "Title updated"})


# DELETE VERSION
@document_bp.route("/version/<int:version_id>", methods=["DELETE"])
def delete_version(version_id):

    version = DocumentVersion.query.get(version_id)

    db.session.delete(version)
    db.session.commit()

    return jsonify({"message": "Version deleted"})


# DELETE DOCUMENT
@document_bp.route("/documents/<int:doc_id>", methods=["DELETE"])
def delete_document(doc_id):

    doc = Document.query.get(doc_id)

    db.session.delete(doc)
    db.session.commit()

    return jsonify({"message": "Document deleted"})


# LIST ALL VERSIONS
@document_bp.route("/documents/<int:doc_id>/versions")
def get_versions(doc_id):

    versions = DocumentVersion.query.filter_by(
        document_id=doc_id
    ).all()

    data = []

    for v in versions:
        data.append({
            "version": v.version_number,
            "user": v.created_by,
            "time": v.created_at
        })

    return jsonify(data)