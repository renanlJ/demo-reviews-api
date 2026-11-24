# demo-reviews-api

Customer reviews microservice for the **Demo Commerce Platform** — a
polyglot reference workload for devex.io (Backstage-based IDP). Returns
reviewer name, review text, rating and creation date per product.

- **Language**: Python 3.12
- **Framework**: FastAPI + uvicorn, pydantic-settings, structlog,
  prometheus-client, OpenTelemetry instrumentation
- **Role**: leaf service consumed by `demo-product-api`
- **Part of**: `system: demo-commerce` / `domain: commerce` (see `catalog-info.yaml`)

## API

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/api/v1/reviews` | All reviews, ordered by creation date |
| GET | `/api/v1/reviews/{productId}` | Reviews for one product (404 if unknown) |
| GET | `/healthz` | Liveness |
| GET | `/readyz` | Readiness (503 when `FAIL_READINESS=true`) |
| GET | `/metrics` | Prometheus text exposition |

OpenAPI contract: [`docs/api/openapi.yaml`](docs/api/openapi.yaml).
Interactive docs at `/docs` (Swagger UI) when running.

## Configuration

| Env var | Default | Description |
| ------- | ------- | ----------- |
| `PORT` | `8000` | Listen port |
| `LOG_LEVEL` | `info` | structlog level |
| `FAIL_READINESS` | `false` | Force `/readyz` → 503 (governance scenario) |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | _(empty)_ | Enable OTLP trace export when set |

## Develop

```bash
make install      # create .venv + install requirements-dev.txt
make test         # pytest (12 tests, ~90% coverage gate)
make lint format  # ruff + bandit + mypy / ruff format --check
make run          # uvicorn app.main:app
```

## Docker

```bash
make docker-build
docker run -p 8000:8000 demo-reviews-api:0.1.0
```

## Kubernetes

```bash
kubectl apply -k deploy/kubernetes
```

## Observability

- JSON logs via structlog with `request_id` and `trace_id` (parsed from
  `traceparent` / `X-Request-ID`).
- Prometheus request counters and latency histograms on `/metrics`.
- Optional OTel HTTP trace export via `OTEL_EXPORTER_OTLP_ENDPOINT`.

## Governance / CI

See `demo-product-api/docs/governance/scenarios.md` and
`.github/workflows/ci.yml` (ruff+pytest+coverage → bandit+pip-audit+
gitleaks+trivy → build → image build+scan → GHCR on `v*` tags).
