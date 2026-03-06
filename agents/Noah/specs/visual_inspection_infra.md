Title: Visual Inspection App — Infrastructure & Deployment Design

Overview:
This document outlines the technical design for deploying the Visual Inspection App. It covers environment topology, CI/CD, container strategy, observability, secrets, and runbooks.

Goals & Constraints:
- Support scalability for backend workloads (stateless API servers, Postgres for stateful data)
- Zero-downtime deployments and easy rollbacks
- Strong observability: Prometheus + Grafana, structured logs
- Infrastructure as code and reproducible builds

Topology:
- Kubernetes cluster (GKE recommended) running app workloads
  - Horizontal Pod Autoscaler on web deployment (minReplicas:2, maxReplicas:10)
  - Managed Postgres (Cloud SQL / RDS) for production
  - External HTTP(S) Load Balancer (managed), TLS termination
  - Internal network with RBAC and least privilege service accounts

Artifacts & Images:
- Multi-stage Dockerfile for small final image (output/config/Dockerfile)
- Container registry: Google Container Registry (gcr) / ECR

CI/CD:
- GitHub Actions for CI (see output/config/.github_workflows_ci.yml)
- Deploy workflow (deploy.yml) will run on merges to main and trigger Terraform apply
- PR checks: pytest gate + ruff + security scan (trivy)

Secrets & Config:
- Use Secret Manager (GCP) or AWS Secrets Manager; never commit .env
- Required GitHub Secrets: DATABASE_URL, SECRET_KEY, RAILWAY_TOKEN, VERCEL_TOKEN
- Runtime config via Kubernetes Secrets and ConfigMaps

Observability & SLOs:
- Prometheus scraping app metrics at /metrics
- Grafana dashboard for p95/p99 latency, error rates, CPU/RAM
- SLOs: Uptime 99.9%, API latency p99 < 500ms
- Alerts: high error rate (>0.1%), high latency (>500ms p99), Pod restart rate

Health checks & Readiness:
- Implement /health (liveness) and /ready (readiness) endpoints
- Load balancer will use /health; k8s readiness gate on /ready

Runbooks:
- P1 outage: Pager duty notify, runbook for database connectivity, roll back deployment

Next steps for Marcus (#ai-backend):
- Implement /health and /ready endpoints in app
- Provide k8s manifests or Helm charts
- Produce API endpoint spec (output/specs/api_endpoints.md)

