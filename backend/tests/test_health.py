"""
Royals Intelligence - Health Probes Test Suite
Verifies GET /health and GET /api/v1/health endpoints.
"""

def test_root_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["project"] == "Royals Intelligence"
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data


def test_api_v1_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["api_version"] == "v1"
    assert data["project"] == "Royals Intelligence"
    assert "components" in data
    assert "database" in data["components"]
    assert "redis" in data["components"]
    assert data["components"]["database"]["engine"] == "postgresql+asyncpg"
