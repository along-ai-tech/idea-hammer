def test_health_endpoint_returns_ok_status(client):
    """健康检查端点返回 ok 状态"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
