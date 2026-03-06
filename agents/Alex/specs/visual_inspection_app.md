# Feature: Visual Inspection App
**Goal:** Provide factory teams an intuitive app for real-time visual inspection that reduces defect escape, speeds inspection, and creates auditable defect records.

**North Star Impact:** Reduce shipped-defect rate by 30% and reduce average inspection time per unit by 25% within 3 months of rollout.

**Users:**
- QA Inspector: visually inspects parts using a camera, needs fast assisted detection + manual annotation.
- Line Operator: runs quick checks and flags issues to maintenance.
- Supervisor / Manager: monitors KPIs and review defect reports.

**RICE Score:**
- Reach = 1,000 inspectors per quarter
- Impact = 2 (performance)
- Confidence = 70% (0.7)
- Effort = 8 person-weeks
- RICE = (1000 × 2 × 0.7) / 8 = 175

**Kano Category:** Performance (significantly improves inspection speed & quality)

**High-level scope:**
- Real-time camera feed with overlayed defect detections
- Manual annotation and correction by inspector
- Persistent defect log with timestamps, images, operator, and metadata
- Dashboard for supervisors with daily/weekly defect summaries
- Mobile-first web app for tablets on the line

**Acceptance Criteria:**
- [ ] Inspector can open camera feed in app, see live overlay boxes/markers for suspected defects
- [ ] Inspector can accept/reject detections and add annotations; changes are saved to backend
- [ ] Each defect saved includes image slice, confidence score, part ID, timestamp, line ID, operator ID
- [ ] Backend exposes APIs for: create defect, list defects (filterable), update defect status, export reports
- [ ] Dashboard shows: defect count by type/line, trend over time, time-to-resolution
- [ ] System handles intermittent connectivity: local queueing on device + eventual sync
- [ ] Performance: overlay latency < 300ms (from frame capture to overlay render) for cloud inference; <100ms target for edge inference
- [ ] Detection model baseline: precision ≥ 88% and recall ≥ 85% on in-scope defect types for v1
- [ ] Security: user auth + role-based access control; image data encrypted at rest

**Out of Scope (v1):**
- Automated mechanical sorting / robotic actuation based on detection
- Full dataset collection & model training pipeline (we will use a provided/third-party model or pre-trained baseline for v1)
- Integration with ERP/WMS beyond simple export endpoints

**Success Metrics:**
- Detection precision and recall vs manual labeling (target precision ≥ 88%, recall ≥ 85%)
- Average inspection time per unit (target -25% vs baseline)
- Adoption rate: % of inspectors using app daily (target ≥ 60%)
- Defect escape rate reduction (target -30% shipped defects)

**Data & Privacy:**
- Images stored for audit for 90 days by default (configurable)
- PII review: ensure no personal data (if present, redact or hash IDs)

**Deployment & infra notes (initial decisions):**
- Start with cloud-hosted inference (faster to iterate). Plan for edge inference as performance improvement path.
- Use WebRTC or MJPEG streaming for low-latency camera feed; fallback to image capture every X seconds for constrained devices.

**Acceptance gating for release:**
- QA signoff on core flows (see acceptance criteria)
- Performance testing: overlay latency under target on test devices
- Security review passed for image storage & auth

**GitHub Issue:** TBD

