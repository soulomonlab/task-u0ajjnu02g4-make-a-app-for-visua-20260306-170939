# Feature: Visual Inspection App (Factory)
**Goal:** Provide factory operators an easy-to-use app that performs automated visual inspection (defect detection) on production lines to reduce inspection time and catch defects earlier.

**North Star Impact:** Reduce manual inspection time and increase defect detection rate to improve first-pass yield.

**Users:**
- Primary: Line operators — need a fast UI to inspect parts and log defects during production.
- Secondary: QA engineers / supervisors — need aggregated reports and exportable defect logs.

**RICE Score:**
- Reach = 200 operators per quarter
- Impact = 2 (measurable productivity improvement)
- Confidence = 80% (0.8)
- Effort = 8 person-weeks
- RICE = (200 × 2 × 0.8) / 8 = 40

**Kano Category:** Performance

**Acceptance Criteria:**
- [ ] User can connect a camera or upload images/videos and run inspection.
- [ ] System runs inference and returns detection results with bounding boxes and confidence scores.
- [ ] UI highlights defects on image/video frames and allows operator to accept/reject and add notes.
- [ ] System logs inspection events and allows export (CSV/JSON) of defect records.
- [ ] Response time for single image inference < 2s (on recommended hardware / edge GPU); streaming / per-frame latency < 500ms where feasible.
- [ ] System handles common edge cases: low-light, motion blur (documented fallback behavior), and network drops (local caching for offline mode).
- [ ] Role-based access: operator vs supervisor with access to aggregated dashboards.

**Out of Scope:**
- Model training pipeline and automated continuous training (initial MVP uses pre-trained/packaged model).
- Full MES/ERP integration beyond export API (MVP exposes a simple REST webhook/API for integration).
- Mobile native apps (web app + kiosk mode only for MVP).

**Success Metrics:**
- Precision >= 85% and Recall >= 80% on target defect classes (measured on validation set).
- Mean time per inspected part reduced by >= 50% vs manual inspection.
- Adoption: 60% of operators in pilot factories use app at least daily within 4 weeks.
- Defect logging reliability: <1% data loss during export.

**Edge Cases & Constraints:**
- Varying lighting and occlusion: include recommended camera placement + configurable brightness/contrast preprocessing.
- High line speed: provide configuration for sampling frequency vs. full-frame inspection.
- Privacy: store images only when defect detected or with operator consent per site policies.

**Implementation Notes / Proposed Tech Choices:**
- Frontend: React web app (kiosk-friendly) with video player overlay for bounding boxes.
- Backend: Python FastAPI for inference + REST API; PostgreSQL for logs; Redis for caching/queue.
- Inference: containerized model running on an edge GPU (NVIDIA Jetson / on-prem server) or cloud GPU for pilot sites without edge hardware.
- Telemetry: basic Prometheus metrics + Sentry for errors.

**GitHub Issue:** TBD (will create and link)

**Acceptance Test Plan (high-level):**
- Manual test: upload 100 labeled test images → verify precision/recall targets.
- Integration test: simulate camera stream → verify frame annotation and UI responsiveness.
- Fault test: simulate network drop → verify local caching and retry on reconnect.

**Success Metrics & Monitoring:**
- Dashboard showing daily inspections, defect counts, precision/recall (from ground-truth sampling), and system latency.

**Outcomes & Next Steps:**
1) Create GitHub issue + backlog tasks (frontend, backend, infra, QA).
2) Detailed API spec and data schema (backend).
3) Design: UI flows and wireframes for operator kiosk (Maya).

