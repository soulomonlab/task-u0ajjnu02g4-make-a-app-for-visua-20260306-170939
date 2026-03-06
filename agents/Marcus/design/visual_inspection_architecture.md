# Visual Inspection App — Technical Architecture

Purpose
- Provide a scalable, observable backend for the Visual Inspection App that supports image uploads, annotation, automated model inference (optional), audit trail, role-based access, and integration points for frontend and QA.

High-level components
1. API Service (FastAPI)
   - Handles auth, user/session, uploads, job creation, annotations, queries.
   - Synchronous endpoints for CRUD and read paths; async background tasks for heavy I/O or CPU-bound work.
   - OpenTelemetry tracing enabled on all incoming requests.

2. PostgreSQL (Primary persistent store)
   - Stores users, projects, inspections, annotations, metadata, audit logs.
   - Recommended extensions: pgcrypto (for token IDs), ltree (if hierarchical tags needed).
   - Indexing strategy in DB Schema section.

3. Object Storage (S3-compatible)
   - Stores original images, thumbnails, LQIP, and any model artifacts.
   - Image URLs stored in DB as presigned URLs when needed.

4. Redis
   - Short-lived caches (thumbnails, recent queries), rate limiting counters, and Celery broker (or use Redis Streams)
   - Store refresh-token rotation IDs and anti-reuse markers.

5. Worker (Celery or RQ)
   - Handles image processing (thumbnail, LQIP generation), calling inference model(s), sending notifications, and background DB writes for heavy operations.
   - Idempotency keys for jobs to prevent double-processing.

6. Optional ML Service
   - If automated inspection/inference is required, separate container/service exposing gRPC/HTTP inference API. Keep model sidecars separate for scaling and memory isolation.

7. Observability
   - OpenTelemetry tracing and metrics (Prometheus + Grafana). Capture spans for uploads, DB queries (>50ms), external calls.
   - Structured logs (JSON) with request_id and trace_id.

8. Security
   - JWT access tokens (15 min) + refresh tokens (7 days) with rotation and reuse detection.
   - RBAC: roles = [admin, engineer, inspector, viewer]; permission checks at service layer.
   - Input validation via Pydantic. Rate limiting (per-IP and per-user) using Redis.
   - CORS configured per environment; cookies SameSite=Lax, Secure, HttpOnly for refresh token.

Scaling & Performance
- API: horizontal autoscaling behind an ingress (ALB / Kubernetes Ingress). Keep endpoints stateless.
- DB: primary with read replicas for heavy read traffic; use connection pooling (asyncpg + SQLAlchemy pool). Max connections tuned to pool * replicas.
- Object storage: scale independently (S3).
- Worker fleet: separate autoscaling based on queue length and CPU/RAM of image processing.
- Caching: use Redis to store precomputed thumbnails and schema-limited query results with TTL 5m.

Data Model (summary)
- users: id (uuid), email, hashed_password, roles (text[]), created_at, updated_at
- projects: id (uuid), owner_id (fk users), name, visibility (private/team/public), created_at
- inspections: id (uuid), project_id, created_by, status(enum), metadata(jsonb), created_at, updated_at
- images: id (uuid), inspection_id, s3_key, width, height, lqip_s3_key, thumbnail_s3_key, uploaded_by, created_at
- annotations: id (uuid), image_id, inspector_id, geometry (geojson), properties (jsonb), created_at, updated_at
- audit_logs: id (uuid), actor_id, action, resource_type, resource_id, detail(jsonb), created_at

Indexing notes
- Index: inspections(project_id, created_at) for recent queries.
- Index: images(inspection_id) and images(created_at) for pagination.
- GIN index on jsonb columns used for querying (annotations.properties)
- Partial indexes for common status values to speed status-based lists.

API surface (summary)
- Auth: /api/v1/auth/* (signup, login, refresh, logout)
- Projects: CRUD /api/v1/projects
- Inspections: CRUD + list /api/v1/projects/:project_id/inspections
- Images: POST /api/v1/inspections/:id/images (multipart/form-data) and GET /api/v1/images/:id
- Annotations: POST/PUT/DELETE /api/v1/images/:id/annotations
- Jobs: GET /api/v1/jobs/:id (background processing status)

Repository & Deployment
- Single repository monolith (backend service) with clear module separation: api (routers), core (business logic), db (models, migrations), workers, tools.
- Dockerized: Dockerfile + docker-compose.dev for local dev (Postgres, Redis, MinIO).
- CI: tests run (pytest) + ruff + mypy + security checks (pip-audit) on PRs.

Operational runbook (brief)
- Revoked refresh-token reuse detected → mark user sessions revoked, require password reset, notify security channel.
- High latencies (>200ms p95) on /images upload → check worker backlog, DB locks, and S3 throughput.

Acceptance criteria for architecture
- Document describes all components and scaling approach (this file).
- Repo scaffold exists (README + folder structure) in repository.
- API endpoints documented in specs/api_endpoints.md and match frontend requirements.

Decisions & trade-offs
- Monolith service: chosen for faster iteration and easier cross-cutting concerns (auth, RBAC). Can split ML inference to separate service later.
- Celery + Redis chosen for ubiquity and reliability; could migrate to Kubernetes Jobs if lower operational overhead desired.

