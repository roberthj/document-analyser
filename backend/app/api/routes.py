from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.document_type import DocumentType
from app.models.report_analysis import ReportAnalysis
from app.services.analyser import analyse_document

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/annual-report/analyse", response_model=ReportAnalysis)
async def analyse_annual_report(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=422, detail="Could not extract text from PDF.")
        # 422 Unprocessable Entity

    return analyse_document(contents, DocumentType.ANNUAL_REPORT)
