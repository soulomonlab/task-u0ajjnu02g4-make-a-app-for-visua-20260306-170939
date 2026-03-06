# Data Contract — Inspection Events

Purpose: Define the event schemas producers must emit for the Visual Inspection App. All events must be JSON and conform to the schema below. Producers should validate before publishing; invalid events go to dead-letter.

Common fields (present in all events):
- event_id: string (uuid)
- event_type: string
- inspection_id: string (uuid)
- event_ts: ISO8601 timestamp
- source: string (mobile|web|edge|backend)
- user_id_pseudo: string (hashed id) — optional for edge/anonymous
- metadata: object (freeform key-values)

Event: inspection_started
- schema:
  - event_type: "inspection_started"
  - inspection_template_id: string
  - started_by: user_id_pseudo
  - location: {lat: number, lon: number} (optional)

Event: image_uploaded
- schema:
  - event_type: "image_uploaded"
  - image_uri: string (gs://... or https://...)
  - camera_id: string
  - resolution: {width:int, height:int}
  - checksum: string (sha256)

Event: defect_detected
- schema:
  - event_type: "defect_detected"
  - model_version: string
  - label: string
  - confidence: float
  - bbox: {x:int,y:int,w:int,h:int}

Event: annotation_saved
- schema:
  - event_type: "annotation_saved"
  - annotated_by: user_id_pseudo
  - labels: [string]
  - severity: string (low|medium|high)
  - bbox: {x:int,y:int,w:int,h:int}

Event: inspection_completed
- schema:
  - event_type: "inspection_completed"
  - completed_by: user_id_pseudo
  - result_summary: object

Validation rules:
- Required fields: event_id, event_type, inspection_id, event_ts
- Timestamps must be ISO8601 and in UTC
- image_uploaded must include image_uri and checksum

Error handling:
- Invalid events -> write to gs://vi-app-deadletter/{YYYY}/{MM}/{DD}/errors.ndjson and publish to dead-letter Pub/Sub topic with error metadata.

Versioning:
- Include data_contract_version in metadata. Increment on any non-backward-compatible change.

