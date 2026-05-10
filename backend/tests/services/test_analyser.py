from unittest.mock import patch

from app.services.analyser import analyse_annual_report

MOCK_RAW_RESULT = {
    "association": {"name": "BRF Testföreningen", "board_members": []},
    "loans": [],
    "summary": "A well-managed association.",
    "notes": [],
}


def test_annual_report_returns_validated_result():
    with (
        patch("app.services.analyser.extract_text", return_value="extracted text"),
        patch("app.services.analyser.run_extraction", return_value=MOCK_RAW_RESULT),
    ):
        result = analyse_annual_report(b"fake pdf bytes")

    assert result.association.name == "BRF Testföreningen"
    assert result.summary == "A well-managed association."
