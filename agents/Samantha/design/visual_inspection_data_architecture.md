# Visual Inspection App — Data Architecture

Summary (deliverable):
- Data architecture and ingestion design for the Visual Inspection App. This document defines sources, sink, storage model, partitioning, retention, monitoring, and data-quality checks to enable Marcus (backend) and DevOps to implement ingestion and storage.

Design decisions (high-level):
- Analytical store: BigQuery (preferred) / Snowflake as fallback. Chosen for near-zero ops, native partitioning, fast analytics for dashboards and ML training.
- Raw data lake: GCS (object storage) for images and raw JSON event logs. Images stored in a controlled bucket with IAM; metadata/events in newline-delimited JSON (NDJSON).
- Ingestion pattern: Event-driven (producer = backend API) -> Pub/Sub (or Kafka) topic -> streaming ingestion to BigQuery via Dataflow or Kafka Connect. Also batch fallback that ingests NDJSON files from GCS.
- Schema-first: Events are defined in a data contract (see output/specs/data_contract_inspection_events.md). Producers must validate before publish.

Data sources:
- Mobile/web client: inspection actions, timestamps, user_id (pseudonymized), location (optional), device metadata.
- Edge device / inspection camera: high-res images uploaded to GCS; metadata events reference image URI and camera_id.
- Manual QA annotations: human-labeled defect tags, severity, bounding boxes.
- Backend systems: job queue, inspection templates, reference data (defect taxonomy).

Core event types (overview):
- inspection_started
- image_uploaded
- defect_detected (automated by vision model)
- annotation_saved (human or model)
- inspection_completed

Storage model (tables):
1) staging.inspection_events_raw (partitioned by ingestion_date)
   - Purpose: landed JSON events for replay and QA.
   - Schema: raw_payload (JSON), event_type (STRING), event_ts (TIMESTAMP), ingestion_ts (TIMESTAMP), source (STRING)
   - Partitioning: ingestion_date
   - Retention: 90 days (configurable)

2) analytics.inspections (partitioned by inspection_date)
   - Purpose: flattened transactional view for product and dashboards.
   - Columns: inspection_id, user_id_pseudo, camera_id, site_id, image_uri, event_type, event_ts, defect_label, severity, bbox, annotation_user, model_confidence, processed_ts
   - Partitioning: inspection_date
   - Clustering: inspection_id, camera_id

3) ml.training_inspections (daily partitioned)
   - Purpose: curated dataset for ML training with image URIs and labels.
   - Stored as external table referencing GCS Parquet/TFRecord

Image storage:
- GCS bucket: gs://vi-app-images/{YYYY}/{MM}/{DD}/{inspection_id}/{image_uuid}.jpg
- Access: Signed URLs for temporarily exposing images to viewers / ML jobs. Images are NOT stored in analytical tables; only URIs are referenced.
- Retention: 180 days standard, configurable per regulation. PII images must be redacted or encrypted.

Partitioning & performance:
- Partition by date (ingestion_date or inspection_date) to support efficient scans.
- Cluster by inspection_id, camera_id for frequent filters.
- Use daily partitions to balance metadata volume and query performance.

Data quality & monitoring:
- Ingest-time validation: JSON schema validation against data contract. Invalid events routed to dead-letter NDJSON in GCS and a monitoring topic.
- Row-count checks: expected events per inspection (e.g., at least 1 image_uploaded + inspection_completed) with alerts when anomalies occur.
- Schema drift detection: nightly job that compares new event keys to expected schema.
- SLA alerts: if Pub/Sub->BigQuery lag > 5 minutes, fire pager.

Access control & PII:
- Pseudonymize user_id at producer (hash with salt stored in secrets manager) to avoid storing raw PII.
- Store location at coarse granularity only (city/region) unless user consent.
- Review with #ai-security (Isabella) for compliance (GDPR, CCPA) before any production rollout.

Operational runbook (brief):
- Data ingestion failure: check Pub/Sub subscription, Dataflow job logs, and GCS dead-letter folder.
- Missing images: correlate analytics.inspections records with image URIs; check GCS bucket permissions.
- Reprocessing: re-ingest from staging.inspection_events_raw by running the batch transformer for the chosen date range.

Open decisions / points for Marcus (backend):
- Confirm whether Pub/Sub or Kafka is used for event transport (we assumed Pub/Sub for GCP).
- Decide if producers will write NDJSON to GCS as a fallback in addition to publishing events.
- Confirm user_id pseudonymization strategy and whether backend or ingest layer will handle hashing.

References:
- Data contract: output/specs/data_contract_inspection_events.md
- Example ETL skeleton: output/code/data/inspection_etl.py

