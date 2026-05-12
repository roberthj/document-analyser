# Document Analyser

AI-powered tool that extracts structured data from PDF documents using Claude API.

## Key decisions
 - Backend: General document analyser that can be extended to other types of documents
 - Frontend: Specific for Annual Reports
 - Enforcing consistent LLM responses using Tool with schema
 - Caching of System Prompt to reduce costs
 - Prompt:
   - Validating the unit (SEK/TSEK)
   - Notes section in response to highlight irregularities
   - Enforcing English language in the response
   - Specific rule for the different dates in the schema

   


## Stack

- **Backend**: Python 3.12, FastAPI, pdfplumber, Anthropic SDK
- **Frontend**: React 18, TypeScript, Vite
- **LLM**: Claude Sonnet 4.6 (structured output via tool use)

## Setup

### Backend

Requires Python 3.12 ([pyenv](https://github.com/pyenv/pyenv) recommended).

```bash
cd backend
python -m venv .venv
source venv/bin/activate
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

| Method | Endpoint | Description                  |
|--------|----------|------------------------------|
| POST | `/annual-report/analyse` | Analyse an annual report PDF |
| GET | `/health` | Health check                 |

