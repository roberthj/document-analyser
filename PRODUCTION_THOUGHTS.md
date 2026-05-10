# From MVP to Production — Architectural Thoughts

## Current State (MVP)

A synchronous FastAPI service that accepts a PDF, extracts text, calls Claude, and returns structured JSON in a single HTTP request. Simple, works well for a demo, but not suitable for production scale.

```
Frontend → FastAPI → Claude API → Response
```

---

## What Would Change in Production

### 1. Persistence Layer (PostgreSQL)

The MVP has no memory — every result is lost after the request. A production service needs a database to:

- Track **job status** (`pending`, `processing`, `completed`, `failed`)
- Store the **extracted structured data** for querying and display
- Store the **prompt and model version** used for each job — for troubleshooting and for future training data
- Log **LLM stats** per job: model, latency, input/output token usage, cost estimate

This makes the system auditable and improvable over time.

---

### 2. Document Storage

- **Object storage** (GCS / S3) for raw PDFs

Upload to storge first.

---

### 2. Async Processing

To be able to scale up a lot we could add async processing via message queues and workers.

The solution would decouple upload from processing:

```
Frontend
  ↓
FastAPI Upload Service     → stores PDF in object storage
  ↓                        → publishes event to Pub/Sub
Returns immediately        → (job_id, status: "processing")
  ↓
AI Worker (separate service)
  ↓  consumes Pub/Sub event
  ↓  extracts + calls Claude
  ↓  stores result in PostgreSQL
  ↓
Frontend polls job_id until status = "completed"
```

**Pub/Sub message example:**
```json
{
  "document_id": "123",
  "storage_path": "gs://annual-reports/123.pdf",
  "document_type": "ANNUAL_REPORT",
  "uploaded_at": "2026-05-10T10:00:00Z"
}
```

This also gives you natural **retry logic** — if the worker crashes, the message stays in the queue and gets reprocessed.

---

### 4. Handling Large Documents

Large documents could be a problem when calling the Anthropic API.

We could solve this by one of following:
- **Selective extraction** — Somehow find only the relevant parts of the annual report before sending them to the LLM.

- **Chunking** — split the document into sections, run separate extractions, merge results.

---

### 5. Model Evaluation Over Time

LLMs improve rapidly — a model released 6 months from now may extract data significantly better. To manage this:

- Store the **model version** and **prompt version** with every job in the database
- Build a small **evaluation set** of reports with known correct extractions
- When considering a model upgrade, run the eval set against the new model and compare accuracy before switching
- The stored prompts also allow **prompt iteration** — you can re-run historical documents with an improved prompt and compare outputs

---

### 6. Repo Structure

For a real production service the frontend and backend should be in separate repos:

- `document-analyser` — the general backend, supports multiple document types
- `annual-report-analyser` — the specific frontend for HoA use case

The backend is designed with this in mind: `DocumentType` enum, type-specific endpoints (`/annual-report/analyse`), and a general extraction layer that any frontend can call.

---

## Architecture Summary

**MVP**
```
FastAPI → Claude API
```

**Production**
```
FastAPI (upload service)
  ↓
Object Storage (GCS/S3)
  ↓
Pub/Sub
  ↓
AI Worker Service → Claude API
  ↓
PostgreSQL
```
