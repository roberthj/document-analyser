from app.clients.claude_client import run_extraction
from app.models.annual_report_analysis import AnnualReportAnalysis
from app.prompts.annual_report_extraction import (
    ANNUAL_REPORT_SYSTEM_PROMPT,
    ANNUAL_REPORT_TOOL_SCHEMA,
    build_annual_report_prompt,
)
from app.utils.pdf import extract_text

def analyse_annual_report(pdf_bytes: bytes) -> AnnualReportAnalysis:
    text = extract_text(pdf_bytes)
    user_prompt = build_annual_report_prompt(text)
    result = run_extraction(user_prompt=user_prompt,                        # The task
                            system_prompt=ANNUAL_REPORT_SYSTEM_PROMPT,      # The rules
                            tool_schema=ANNUAL_REPORT_TOOL_SCHEMA)          # The response structure

    return AnnualReportAnalysis.model_validate(result)
