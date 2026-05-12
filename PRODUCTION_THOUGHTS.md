# From MVP to Production

## What Would I Change in Production

---

### 1. Decouple Upload from Processing

To be able to scale up a lot we could add async processing via message queues and workers.

Upload to Storage and put a message on a queue for processing

- **Object storage** (GCS / S3) for raw PDFs


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

### 2. Persistence Layer (PostgreSQL)

A production service needs a database to:

- Track **job status** (`pending`, `processing`, `completed`, `failed`)
- Store the **extracted structured data** for querying and display
- Store the prompt version, model, latency, token usage, and cost estimate per job — for troubleshooting, cost visibility, and future training data.

---

### 3. Handling Large Documents

Large documents could be a problem and could cause when calling the Anthropic API.

We could solve this by one of following:
- **Selective extraction** — Somehow find only the relevant parts of the annual report before sending them to the LLM.
  - This could reduce cost as well.

- **Chunking** — split the document into sections, run separate extractions, merge results.

---

### 4. Model Evaluation Over Time

- Store the **model version** and **prompt version** with every job in the database
- Build a small **evaluation set** of reports with known correct extractions
- Use to evaluate existing and new models

---
