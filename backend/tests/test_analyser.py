from unittest.mock import patch

import pytest

from app.models.document import DocumentType
from app.services.analyser import analyse_document

MOCK_RAW_RESULT = {
    "association": {"name": "BRF Testföreningen", "board_members": []},
    "loans": [],
    "summary": "A well-managed association.",
}


def test_annual_report_returns_validated_result():
    with (
        patch("app.services.analyser.extract_text", return_value="extracted text"),
        patch("app.services.analyser.run_extraction", return_value=MOCK_RAW_RESULT),
    ):
        result = analyse_document(b"fake pdf bytes", DocumentType.ANNUAL_REPORT)

    assert result.association.name == "BRF Testföreningen"
    assert result.summary == "A well-managed association."


def test_unsupported_document_type_raises():
    with pytest.raises(ValueError, match="Unsupported document type"):
        analyse_document(b"fake pdf bytes", "UNSUPPORTED")
