"""health endpoint 测试（TDD RED 起点）"""
from fastapi.testclient import TestClient


def test_health_endpoint_returns_ok_status(client: TestClient):
    """GET /api/health 应返回 {status: ok}"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}