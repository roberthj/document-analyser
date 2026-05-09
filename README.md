# Annual Report Analyser

AI-powered tool that extracts structured data from Homeowners Association (HoA) annual report PDFs using Claude.

## Stack

- **Backend**: Python, FastAPI, pdfplumber, Anthropic SDK
- **Frontend**: React 18, TypeScript, Vite
- **LLM**: Claude claude-sonnet-4-6 (structured output via tool use)

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

## Usage

1. Start both backend and frontend
2. Open http://localhost:5173
3. Upload a HoA annual report PDF
4. The app extracts and displays: association facts, board members, loans

## Project structure

```
backend/
  app/
    main.py              # FastAPI app factory, middleware, router
    api/
      routes.py          # Thin route handlers
    models/
      report.py          # Pydantic schemas
    services/
      analyser.py        # Orchestration (PDF → LLM → result)
    clients/
      anthropic.py       # Anthropic API wrapper
    prompts/
      report.py          # System + user prompt strings
    utils/
      pdf.py             # PDF text extraction

frontend/src/
  App.tsx
  types.ts
  components/
    FileUpload.tsx        # Drag-and-drop upload
    ReportResult.tsx      # Display extracted data
```
