import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_analysis():
    from app.models.report import AssociationFacts, ReportAnalysis
    return ReportAnalysis(
        association=AssociationFacts(name="BRF Testföreningen"),
        loans=[],
        summary="A well-managed association with no outstanding loans.",
    )
