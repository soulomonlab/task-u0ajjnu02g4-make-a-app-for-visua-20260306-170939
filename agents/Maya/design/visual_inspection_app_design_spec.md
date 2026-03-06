# Visual Inspection App — Design Specification

Owner: Maya (Designer)
Date: 2026-03-06

Purpose
- Provide a concise but complete UX spec for the Visual Inspection App so engineering can start UI implementation.
- Deliverables: user flow, wireframes (ASCII), component specs, interaction rules, accessibility and constraints.

Audience
- Frontend engineer (Kevin) — primary receiver
- Backend engineer (Marcus) — notes on UI-driven constraints

1) Core product flows (high level)
- Inspect Item
  1. Inspector selects an item from list or scans QR
  2. Opens item detail → image viewer with latest capture and history
  3. Create inspection: capture/upload photo(s), annotate (bounding boxes, freehand), set pass/fail, add tags/notes, save
  4. Save triggers upload + optional sync to server; inspector sees success state and next recommended item

- Review History
  - View chronological list of inspections per item; filter by date, inspector, result

- Bulk Review
  - QA lead can quickly see failed items, open each, reassign or escalate

2) User personas & context
- Floor inspector: mobile-first, one-handed use, fast captures, offline-capable
- QA lead: desktop-first, needs filters, batch actions, larger canvas for annotations

Decision: prioritize mobile-first capture flow and desktop-first review flow. This is reversible by making components responsive.

3) Requirements & constraints impacting UI (from product/backend)
- Image max size: recommend 5MB compressed upload (note to backend: provide server-side resizing)
- Offline capture: store pending inspections locally (frontend to implement local storage/sync)
- API: image upload endpoints should accept multipart/form-data and return image_id
- Latency: show optimistic UI for save with progress indicator

4) Wireframes (ASCII) — mobile (primary) and desktop

Mobile — Inspect Flow

[Top Nav: ← Item Name | •••]

[IMAGE VIEWER]
|------------------------------|
|  Photo (full-bleed)          |
|  (tap to annotate / pinch)   |
|------------------------------|

[Toolbar: Capture | Upload | Annotate | Flash ]

[Result toggle: PASS (green) | FAIL (red) ]

[Tags input]  [Note (optional)]

[Save Button (primary, full-width)]

Desktop — Review Grid

[Sidebar: Filters | Search ]  [Main: Grid of item cards]
Card -> Thumbnail | Item ID | Last result | Quick actions

Detail modal: Large image viewer (left) | Metadata + history (right)
Annotation tools along top: Rect | Brush | Arrow | Text | Undo | Export

5) Component specs
- Primary button
  - States: default, pressed, disabled
  - Mobile: full-width, 48px height, border-radius 8px
  - Color: Primary (#0A64FF) text white
- Secondary button (outline)
- Result toggle (Pass/Fail)
  - Two-segment segmented control. Pass=green (#20C997). Fail=red (#FF4D4F)
  - Accessibility: each segment ARIA-pressed, contrast >= 4.5:1
- Image viewer
  - Full-bleed on mobile, responsive container on desktop
  - Supports pinch-zoom, double-tap to zoom, pan
  - Annotation overlay: vector layer (SVG) with selectable shapes; max 20 objects
- Annotation tools
  - Rect tool: click-drag to create box. Metadata modal for each shape: label, severity (Low/Med/High), color
  - Brush tool: freehand strokes, smoothing enabled
  - Undo/redo stack (20 entries)
- Tag input
  - Autocomplete suggestions from backend; create new tag on enter
- Offline indicator
  - Small chip near top left showing sync status (Synced / Pending • N)

6) Interaction rules & edge-cases
- If user attempts Save while offline → enqueue save locally, show toast "Saved locally — will sync when online". Provide Retry button on failed uploads.
- If annotation creation collides with existing object → show snap/overlap tooltip and ask to confirm merge or keep separate.
- When switching items while unsaved changes exist → prompt: Save / Discard / Cancel
- Deleting an inspection requires confirmation; move to trash for 24h before permanent delete (product decision)

7) Accessibility
- All actionable items must be reachable by keyboard on desktop
- Color choices must meet contrast 4.5:1 (we recommend testing) — provide accessible focus outlines
- Annotations must have textual alternatives (e.g., label + severity) for export

8) Visual tokens (initial)
- Typography: Inter Regular 16px body; H1 28px bold; H2 20px semi-bold
- Spacing: base unit 8px
- Colors:
  - Primary: #0A64FF
  - Success: #20C997
  - Danger: #FF4D4F
  - Surface: #FFFFFF
  - Muted text: #6B7280

Decision: Keep token set minimal to avoid heavy design system work at launch; extend after v1.

9) Acceptance criteria (for design -> implementation handoff)
- Frontend implements mobile inspect flow with capture, annotate, pass/fail, tags, save.
- Image viewer supports pinch-zoom, annotation overlay, and undo/redo.
- Offline save queue visible and sync status shown.
- Desktop review has filters and detail modal with history.

10) Handoff notes for backend (Marcus)
- Provide API endpoints: upload image (multipart), create inspection (JSON with image_id + annotations), list inspections (filters), get inspection detail
- Return image_id and thumbnail URL on upload
- Provide tag suggestions endpoint
- For offline: endpoints must support idempotency keys for retries

11) Implementation risks & mitigations
- Annotation performance on low-end mobile: mitigate by rasterizing heavy vector layers after edit and limiting stroke points (smoothing)
- Large image uploads: request server-side resizing and client-side compression

12) Files / assets
- This spec (visual_inspection_app_design_spec.md)
- Placeholder mockups: not included here — request from #ai-design if needed.

13) Next steps
- Frontend (Kevin): implement components and mobile flow per spec; create Storybook stories for each component and a demo page for the inspect flow.
- Backend (Marcus): confirm API endpoints and constraints called out in section 10.

Design decisions log
- Mobile-first capture prioritized to reduce inspector friction.
- Minimal token set to accelerate delivery; full design system deferred.

---

End of spec.
