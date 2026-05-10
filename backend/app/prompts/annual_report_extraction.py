ANNUAL_REPORT_SYSTEM_PROMPT = """
You are an expert at extracting structured data from Homeowners Association (HoA) annual reports.
The document may be written in Swedish or English.

Rules:
- Extract only what is explicitly stated in the document. Do not infer or guess.
- If a field is not present, return null.
- For loans, only include entries clearly described as formal loans or credit facilities
  (e.g. from a bank or lender). Exclude informal mentions.
- The summary should be 2-3 plain-language sentences aimed at a non-expert homeowner.
- For interest rates, include the full description as a string (e.g. "Stibor + 1.2%").
- For maturity dates, use the format stated in the document (e.g. "2026-03-31").
- The response should be in english only. Do not show the original text from any other language.

When analyzing financial statements:

- Always perform consistency and reasonableness checks across the document.
- Prioritize tables and notes over descriptive text when values conflict.
- Validate monetary amounts against related figures such as:
    - total assets
    - interest expense
    - debt per sqm
    - prior years
- If a unit label (e.g. SEK, TSEK, MSEK) creates clearly unreasonable values, assume the label may be incorrect and choose the interpretation most consistent with the rest of the financial statements.
- Explicitly flag suspected unit or formatting errors.
""".strip()

ANNUAL_REPORT_TOOL_SCHEMA = {
    "name": "extract_report_data",
    "description": "Extract structured data from a HoA annual report.",
    "input_schema": {
        "type": "object",
        "properties": {
            "association": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "organization_number": {"type": ["string", "null"]},
                    "address": {"type": ["string", "null"]},
                    "num_apartments": {"type": ["integer", "null"]},
                    "board_members": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "role": {"type": "string"},
                            },
                            "required": ["name", "role"],
                        },
                    },
                },
                "required": ["name", "board_members"],
            },
            "loans": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "lender": {"type": "string"},
                        "amount": {"type": ["number", "null"]},
                        "currency": {"type": ["string", "null"]},
                        "interest_rate": {"type": ["string", "null"]},
                        "maturity_date": {"type": ["string", "null"]},
                    },
                    "required": ["lender"],
                },
            },
            "summary": {"type": "string"},
            "notes": {
                "type": "array",
                "description": "List of flagged inconsistencies, suspected unit errors, or other irregularities found in the document. Empty if none found.",
                "items": {"type": "string"},
            },
        },
        "required": ["association", "loans", "summary", "notes"],
    },
}


def build_annual_report_prompt(text: str) -> str:
    return (
        "Please extract the key information from the following annual report.\n\n"
        "---\n"
        f"{text}\n"
        "---\n\n"
        "Call the run_extraction tool with the structured data."
    )
