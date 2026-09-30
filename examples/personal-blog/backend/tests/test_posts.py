"""Post CRUD + 置顶 端点测试（TDD RED 起点）
测试名回答"什么 break 让它失败"。
"""
from fastapi.testclient import TestClient


def _create_post(client: TestClient, title="默认标题", content="默认内容", is_pinned=False):
    """辅助：POST 创建一篇博客"""
    return client.post(
        "/api/posts",
        json={"title": title, "content": content, "is_pinned": is_pinned},
    )


# ---------- F-2.1 POST /api/posts ----------

def test_create_post_returns_201_with_id_and_slug(client: TestClient):
    """创建博客应返回 201 + id + slug + 必填字段"""
    response = _create_post(client, title="我的第一篇博客", content="Hello World")
    assert response.status_code == 201
    data = response.json()
    assert data["id"] >= 1
    assert data["slug"] == "我的第一篇博客"  # 默认 slug 从 title 生成
    assert data["title"] == "我的第一篇博客"
    assert data["content"] == "Hello World"
    assert data["is_pinned"] is False


def test_create_post_with_empty_title_returns_422(client: TestClient):
    """空 title 应被 Pydantic 拦截，返回 422"""
    response = _create_post(client, title="", content="x")
    assert response.status_code == 422


def test_create_post_with_empty_content_returns_422(client: TestClient):
    """空 content 应被 Pydantic 拦截，返回 422"""
    response = _create_post(client, title="x", content="")
    assert response.status_code == 422


# ---------- F-2.2 GET /api/posts ----------

def test_list_posts_returns_all_with_pinned_first(client: TestClient):
    """列表：置顶博客应排在最前"""
    _create_post(client, title="普通 1", content="x")
    _create_post(client, title="普通 2", content="x")
    pinned = _create_post(client, title="置顶篇", content="y", is_pinned=True).json()

    response = client.get("/api/posts")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 3
    assert items[0]["id"] == pinned["id"]  # 置顶在最前
    assert items[0]["is_pinned"] is True


def test_list_posts_supports_pagination(client: TestClient):
    """列表应支持分页（limit + offset）"""
    for i in range(5):
        _create_post(client, title=f"博客 {i}", content="x")

    response = client.get("/api/posts?limit=2&offset=0")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2


# ---------- F-2.3 GET /api/posts/{id_or_slug} ----------

def test_get_post_by_id_returns_full_content(client: TestClient):
    """按 id 查博客应返回完整 content"""
    created = _create_post(client, title="查我", content="完整内容").json()

    response = client.get(f"/api/posts/{created['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["content"] == "完整内容"


def test_get_post_by_slug_returns_same_post(client: TestClient):
    """按 slug 查博客应跟按 id 等价"""
    created = _create_post(client, title="slug-查我", content="x").json()

    response = client.get(f"/api/posts/{created['slug']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_nonexistent_post_returns_404(client: TestClient):
    """不存在的 id 应返回 404，非 500"""
    response = client.get("/api/posts/9999")
    assert response.status_code == 404


# ---------- F-2.4 PUT /api/posts/{id} ----------

def test_update_post_changes_title_and_content(client: TestClient):
    """PUT 应能改 title + content"""
    created = _create_post(client, title="旧标题", content="旧内容").json()

    response = client.put(
        f"/api/posts/{created['id']}",
        json={"title": "新标题", "content": "新内容", "is_pinned": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "新标题"
    assert data["content"] == "新内容"


# ---------- F-2.5 DELETE /api/posts/{id} ----------

def test_delete_post_returns_204_and_subsequent_get_returns_404(client: TestClient):
    """删除后 GET 应返回 404"""
    created = _create_post(client, title="要删", content="x").json()

    delete_response = client.delete(f"/api/posts/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/posts/{created['id']}")
    assert get_response.status_code == 404


# ---------- F-2.8 PATCH /api/posts/{id}/pin ----------

def test_pin_post_toggles_is_pinned(client: TestClient):
    """PATCH pin 应翻转 is_pinned"""
    created = _create_post(client, title="要置顶", content="x").json()
    assert created["is_pinned"] is False

    response = client.patch(f"/api/posts/{created['id']}/pin")
    assert response.status_code == 200
    assert response.json()["is_pinned"] is True

    response = client.patch(f"/api/posts/{created['id']}/pin")
    assert response.status_code == 200
    assert response.json()["is_pinned"] is False


# ---------- WI-5 F-2.3 详情端点聚合 ----------

def test_get_post_detail_includes_comments(client: TestClient):
    """详情端点应返回评论列表（含 nickname / content / created_at）"""
    post = _create_post(client, title="有评论的博客", content="x").json()
    client.post(f"/api/posts/{post['id']}/comments", json={"nickname": "alice", "content": "1"})
    client.post(f"/api/posts/{post['id']}/comments", json={"nickname": "bob", "content": "2"})

    data = client.get(f"/api/posts/{post['id']}").json()
    assert len(data["comments"]) == 2
    nicknames = {c["nickname"] for c in data["comments"]}
    assert nicknames == {"alice", "bob"}
    contents = {c["content"] for c in data["comments"]}
    assert contents == {"1", "2"}


def test_get_post_detail_includes_up_and_down_counts(client: TestClient):
    """详情端点应返回 up_count / down_count"""
    post = _create_post(client, title="有反应的博客", content="x").json()
    h1 = {"X-Forwarded-For": "1.1.1.1"}
    h2 = {"X-Forwarded-For": "2.2.2.2"}
    h3 = {"X-Forwarded-For": "3.3.3.3"}

    client.post(f"/api/posts/{post['id']}/react", json={"type": "up"}, headers=h1)
    client.post(f"/api/posts/{post['id']}/react", json={"type": "up"}, headers=h2)
    client.post(f"/api/posts/{post['id']}/react", json={"type": "down"}, headers=h3)

    data = client.get(f"/api/posts/{post['id']}").json()
    assert data["up_count"] == 2
    assert data["down_count"] == 1


def test_get_post_detail_returns_empty_collections_when_no_interactions(client: TestClient):
    """无评论无反应的博客详情应返回空 collections + 全 0"""
    post = _create_post(client, title="孤博客", content="x").json()
    data = client.get(f"/api/posts/{post['id']}").json()
    assert data["comments"] == []
    assert data["up_count"] == 0
    assert data["down_count"] == 0