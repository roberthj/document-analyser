# Document Analyser

AI-powered tool that extracts structured data from PDF documents using Claude.

## Stack

- **Backend**: Python, FastAPI, pdfplumber, Anthropic SDK
- **Frontend**: React 18, TypeScript, Vite
- **LLM**: Claude Sonnet 4.6 (structured output via tool use)

## Setup

### Backend

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your ANTHROPIC_API_KEY
uvicorn app.main:app --reload
```

API runs on http://localhost:8000 — Swagger docs at http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

UI runs on http://localhost:5173

### Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

## Usage

1. Start both backend and frontend
2. Open http://localhost:5173
3. Upload a PDF document
4. The app extracts and displays: association facts, board members, loans

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/annual-report/analyse` | Analyse a HoA annual report PDF |
| GET | `/health` | Health check |

## Project structure

```
backend/
  app/
    main.py              # FastAPI app factory, middleware, router
    api/
      routes.py          # Route handlers
    models/
      document_type.py   # DocumentType enum
      report_analysis.py # Pydantic schemas (ReportAnalysis, Loan, etc.)
    services/
      analyser.py        # Orchestration (PDF → LLM → result)
    clients/
      claude_client.py   # Anthropic API wrapper
    prompts/
      annual_report_extraction.py  # System prompt, tool schema, user prompt builder
    utils/
      pdf.py             # PDF text extraction
  tests/
    conftest.py          # Shared pytest fixtures
    test_routes.py       # Endpoint tests
    test_analyser.py     # Service tests

frontend/src/
  App.tsx
  types.ts
  components/
    FileUpload.tsx        # Drag-and-drop upload
    ReportResult.tsx      # Display extracted data
```
