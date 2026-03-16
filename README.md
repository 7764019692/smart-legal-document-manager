## User Guide

Follow the steps below to run and test the Smart Legal Document Manager.

### 1. Install Dependencies

Run the following command:

pip install -r requirements.txt

### 2. Start the Application

Run:

python run.py

The server will start at:

http://127.0.0.1:5000

You can test the APIs using Thunder Client, Postman, or curl.

---

### 3. Create a Document

Endpoint:

POST /documents

Example Request Body:

{
"title": "Employment Contract",
"text": "This contract is between employer and employee.",
"user": "Satyaki"
}

This will create a new document and store the first version.

---

### 4. Create a New Version

Endpoint:

POST /documents/{document_id}/version

Example Request Body:

{
"text": "This contract is between employer and employee. Payment due in 30 days.",
"user": "Satyaki"
}

This creates a new version without overwriting the previous one.

---

### 5. Compare Two Versions

Endpoint:

GET /documents/{document_id}/compare?v1=1&v2=2

This compares version 1 and version 2 of the document and returns the differences.

---

### 6. Update Document Title

Endpoint:

PATCH /documents/{document_id}/title

Example Request Body:

{
"title": "Updated Employment Contract"
}

This updates only the title without creating a new document version.

---

### 7. Delete a Version

Endpoint:

DELETE /version/{version_id}

This removes a specific document version without deleting the entire document.

---

### 8. Delete a Document

Endpoint:

DELETE /documents/{document_id}

This deletes the document and all associated versions.

---

### 9. View All Versions

Endpoint:

GET /documents/{document_id}/versions

This returns all stored versions along with the user and timestamp.
