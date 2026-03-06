Visual Inspection App — API Endpoint Specification

Base URL: /api/v1

Authentication:
- Token-based (Bearer). Further decision: use JWT (short expiry) or opaque tokens (revocable). Marcus to choose.

Endpoints:
1) POST /api/v1/sessions
   - Purpose: create a user session (login)
   - Body: {"email": "...", "password": "..."}
   - Responses: 200 {"token":"..."}, 401 unauthorized

2) GET /api/v1/inspections
   - Purpose: list inspections
   - Query: page, per_page, status
   - Responses: 200 [{inspection_objects}]

3) GET /api/v1/inspections/{id}
   - Purpose: retrieve a single inspection
   - Responses: 200 {inspection}, 404 not found

4) POST /api/v1/inspections
   - Purpose: create inspection record (metadata + image upload)
   - Body: multipart/form-data {metadata JSON, file image}
   - Responses: 201 {id, status}, 400 validation errors

5) POST /api/v1/inspections/{id}/results
   - Purpose: submit inspection results (human or ML model)
   - Body: {"result": "pass|fail", "notes": "..."}
   - Responses: 200, 404

6) GET /api/v1/health
   - Purpose: liveness check
   - Responses: 200 {"status":"ok"}

7) GET /api/v1/ready
   - Purpose: readiness check (DB connectivity)
   - Responses: 200 {"status":"ready"} or 503

Non-functional requirements:
- p99 < 500ms for read endpoints under normal load
- Uploads stored in object storage (GCS/S3)
- All responses JSON except file uploads

Next actions for Marcus (#ai-backend):
- Choose auth approach (JWT vs opaque). Implement token handling.
- Implement /health and /ready endpoints and document in code.
- Add OpenAPI schema (preferred) for these endpoints.
