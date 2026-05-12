from unittest.mock import patch


def test_rejects_non_pdf(client):
    response = client.post(
        "/annual-report/analyse",
        files={"file": ("report.txt", b"not a pdf", "text/plain")},
    )
    assert response.status_code == 400


def test_rejects_empty_file(client):
    response = client.post(
        "/annual-report/analyse",
        files={"file": ("report.pdf", b"", "application/pdf")},
    )
    assert response.status_code == 422


def test_returns_analysis_for_valid_pdf(client, mock_analysis):
    with patch("app.api.routes.analyse_annual_report", return_value=mock_analysis):
        response = client.post(
            "/annual-report/analyse",
            files={"file": ("report.pdf", b"%PDF-fake", "application/pdf")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["association"]["name"] == "BRF Testföreningen"
    assert data["summary"] == "A well-managed association with no outstanding loans."


def test_returns_500_when_claude_returns_no_tool_block():
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app, raise_server_exceptions=False) as client:
        with patch("app.api.routes.analyse_annual_report", side_effect=ValueError("Claude did not return a tool use block")):
            response = client.post(
                "/annual-report/analyse",
                files={"file": ("report.pdf", b"%PDF-fake", "application/pdf")},
            )
    assert response.status_code == 500
