Visual Inspection App — Repo README

Repository layout (initial):

- src/                # Python application source
- tests/              # Pytest test suite
- output/             # Generated artifacts
- Dockerfile          # Multi-stage Dockerfile (output/config/Dockerfile)
- docker-compose.yml  # Local compose for dev (output/config/docker-compose.yml)
- .github/workflows/  # CI workflows (output/config/.github_workflows_ci.yml)

Development
-----------
- Create a virtualenv: python -m venv .venv
- Install dev deps: pip install -r requirements.txt
- Run tests: python -m pytest tests/
- Run locally with docker-compose: docker-compose up --build

Health endpoints
----------------
- /health — liveness probe (returns 200 when app process up)
- /ready  — readiness probe (checks DB connectivity and migrations)

CI/CD
-----
- PRs run pytest and ruff. Main branch builds Docker image.
- Deploy workflow will be created to apply Terraform and update k8s.

Contributing
------------
Follow conventional commits. Add unit tests for new features. Update API specs in output/specs/api_endpoints.md when changing endpoints.
