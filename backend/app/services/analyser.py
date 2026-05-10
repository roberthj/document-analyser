from pydantic import BaseModel

from app.clients.claude_client import run_extraction
from app.models.document_type import DocumentType
from app.models.report_analysis import ReportAnalysis
from app.prompts.annual_report_extraction import (
    ANNUAL_REPORT_SYSTEM_PROMPT,
    ANNUAL_REPORT_TOOL_SCHEMA,
    build_annual_report_prompt,
)
from app.utils.pdf import extract_text


def analyse_document(pdf_bytes: bytes, document_type: DocumentType) -> BaseModel:
    if document_type == DocumentType.ANNUAL_REPORT:
        system_prompt = ANNUAL_REPORT_SYSTEM_PROMPT
        tool_schema = ANNUAL_REPORT_TOOL_SCHEMA
        build_prompt = build_annual_report_prompt
        result_model = ReportAnalysis
    else:
        raise ValueError(f"Unsupported document type: {document_type}")

    text = extract_text(pdf_bytes)
    result = run_extraction(build_prompt(text), system_prompt, tool_schema)
    return result_model.model_validate(result)      # Converts to ReportAnalysis object
