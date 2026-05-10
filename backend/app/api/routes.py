from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.annual_report_analysis import AnnualReportAnalysis
from app.services.analyser import analyse_annual_report

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/annual-report/analyse", response_model=AnnualReportAnalysis)
async def annual_report_analyse(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=422, detail="Could not extract text from PDF.")

    return analyse_annual_report(contents)
