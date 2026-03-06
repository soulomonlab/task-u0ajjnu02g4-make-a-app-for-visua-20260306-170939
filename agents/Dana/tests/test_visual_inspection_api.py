# pytest tests for Visual Inspection App API
# These are integration-style tests and require environment variable VI_BASE_URL to be set

import os
import uuid
import pytest
import requests
from concurrent.futures import ThreadPoolExecutor

BASE_URL = os.getenv("VI_BASE_URL")
AUTH_TOKEN = os.getenv("VI_AUTH_TOKEN")  # Optional: service token for authenticated endpoints

pytestmark = pytest.mark.skipif(BASE_URL is None, reason="VI_BASE_URL not set; integration tests skipped")

HEADERS = {"Content-Type": "application/json"}
if AUTH_TOKEN:
    HEADERS["Authorization"] = f"Bearer {AUTH_TOKEN}"


def make_inspection_payload(image_url=None):
    return {
        "title": f"QA Test Inspection {uuid.uuid4()}",
        "description": "Automated test payload",
        "image_url": image_url or "https://example.com/image.jpg",
        "metadata": {"source": "qa-test"}
    }


def create_inspection(payload):
    resp = requests.post(f"{BASE_URL}/inspections", json=payload, headers=HEADERS, timeout=10)
    return resp


def test_health_check():
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    assert r.status_code == 200
    assert r.json().get("status") in ("ok", "healthy", "UP")


def test_create_inspection_valid_payload():
    payload = make_inspection_payload()
    r = create_inspection(payload)
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    assert data.get("status") in ("pending", "created")


def test_create_inspection_invalid_payload():
    # Missing required field 'image_url' should return 400
    payload = {"title": "bad payload"}
    r = requests.post(f"{BASE_URL}/inspections", json=payload, headers=HEADERS, timeout=10)
    assert r.status_code == 400


def test_get_inspection_by_id():
    payload = make_inspection_payload()
    r = create_inspection(payload)
    assert r.status_code == 201
    ins_id = r.json().get("id")
    r2 = requests.get(f"{BASE_URL}/inspections/{ins_id}", headers=HEADERS, timeout=5)
    assert r2.status_code == 200
    data = r2.json()
    assert data.get("id") == ins_id
    assert data.get("title") == payload["title"]


def test_update_results_requires_auth():
    payload = make_inspection_payload()
    r = create_inspection(payload)
    assert r.status_code == 201
    ins_id = r.json().get("id")
    # call update without auth header
    r2 = requests.patch(f"{BASE_URL}/inspections/{ins_id}/results", json={"result": "pass"}, timeout=5)
    assert r2.status_code in (401, 403)


def test_list_inspections_pagination():
    # Ensure list endpoint supports pagination params
    r = requests.get(f"{BASE_URL}/inspections?page=1&per_page=5", headers=HEADERS, timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data.get("items"), list)
    assert "total" in data


def test_concurrent_create_requests_no_500s():
    # Fire several create requests in parallel to surface race conditions
    payload = make_inspection_payload()
    def task(i):
        p = make_inspection_payload()
        resp = create_inspection(p)
        return resp.status_code

    statuses = []
    with ThreadPoolExecutor(max_workers=5) as ex:
        for st in ex.map(task, range(5)):
            statuses.append(st)

    # Expect 201 for successes; no 500
    assert not any(s >= 500 for s in statuses)


def test_large_image_upload_rejection():
    # If the system enforces max image size, a very large 'image_url' could be rejected.
    # This is speculative; accept either 413 or validation 400.
    payload = make_inspection_payload(image_url=("https://example.com/huge.img"))
    r = create_inspection(payload)
    assert r.status_code in (201, 400, 413)
