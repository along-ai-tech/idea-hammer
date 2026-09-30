"""Reaction endpoints（WI-4：点赞 / 点踩 + 防重复）

端点：
- POST /api/posts/{post_id}/react   EP-7, F-2.7 点赞/点踩
- GET  /api/posts/{post_id}/reactions   顺手：返回该博客的 up/down 计数

防重复（Design-Brief / DEV-PLAN §5）：
- UNIQUE(post_id, ip) 数据库约束
- 同 IP 重复同 type → 计数不变（返回现有 row）
- 同 IP 切换 type → 删旧 + 增新（v0 toggle 语义）
"""
from fastapi.testclient import TestClient


# ---------- F-2.7 POST /api/posts/{id}/react ----------

def test_react_up_creates_row_and_returns_counts(client: TestClient):
    """首次点赞应创建一行 + 返回当前 up/down 计数"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()

    response = client.post(
        f"/api/posts/{post['id']}/react",
        json={"type": "up"},
        headers={"X-Forwarded-For": "1.2.3.4"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["post_id"] == post["id"]
    assert data["up_count"] == 1
    assert data["down_count"] == 0


def test_react_down_creates_row(client: TestClient):
    """首次点踩：up=0 down=1"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()
    response = client.post(
        f"/api/posts/{post['id']}/react",
        json={"type": "down"},
        headers={"X-Forwarded-For": "5.6.7.8"},
    )
    assert response.status_code == 200
    assert response.json()["down_count"] == 1


def test_same_ip_react_up_twice_does_not_double_count(client: TestClient):
    """同 IP 重复点赞 → 计数仍是 1（UNIQUE 防重）"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()
    h = {"X-Forwarded-For": "1.2.3.4"}

    r1 = client.post(f"/api/posts/{post['id']}/react", json={"type": "up"}, headers=h)
    r2 = client.post(f"/api/posts/{post['id']}/react", json={"type": "up"}, headers=h)

    assert r1.json()["up_count"] == 1
    assert r2.json()["up_count"] == 1  # 仍是 1


def test_same_ip_switch_up_to_down_replaces_reaction(client: TestClient):
    """同 IP 从 up 切换到 down → up=0 down=1（v0 toggle 语义：删旧增新）"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()
    h = {"X-Forwarded-For": "1.2.3.4"}

    r1 = client.post(f"/api/posts/{post['id']}/react", json={"type": "up"}, headers=h)
    assert r1.json()["up_count"] == 1

    r2 = client.post(f"/api/posts/{post['id']}/react", json={"type": "down"}, headers=h)
    assert r2.json()["up_count"] == 0
    assert r2.json()["down_count"] == 1


def test_different_ips_can_both_react_up(client: TestClient):
    """不同 IP 各点一次 up → up=2"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()
    r1 = client.post(
        f"/api/posts/{post['id']}/react",
        json={"type": "up"},
        headers={"X-Forwarded-For": "1.1.1.1"},
    )
    r2 = client.post(
        f"/api/posts/{post['id']}/react",
        json={"type": "up"},
        headers={"X-Forwarded-For": "2.2.2.2"},
    )
    assert r1.json()["up_count"] == 1
    assert r2.json()["up_count"] == 2


def test_react_with_invalid_type_returns_422(client: TestClient):
    """type 不是 up/down → 422"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()
    response = client.post(
        f"/api/posts/{post['id']}/react",
        json={"type": "sideways"},
        headers={"X-Forwarded-For": "1.1.1.1"},
    )
    assert response.status_code == 422


def test_react_on_nonexistent_post_returns_404(client: TestClient):
    """对不存在的博客 react 应 404"""
    response = client.post(
        "/api/posts/9999/react",
        json={"type": "up"},
        headers={"X-Forwarded-For": "1.1.1.1"},
    )
    assert response.status_code == 404