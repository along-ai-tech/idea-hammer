"""Comment endpoints（WI-3：POST 评论 + DELETE 评论）

端点：
- POST   /api/posts/{post_id}/comments   创建评论（EP-6, F-2.6）
- DELETE /api/comments/{comment_id}      删除评论（EP-9, F-2.9）

约束（Design-Brief §comments）：
- content 不能为空
- post_id 必存在（外键 → Post.id，Post 删除则级联删评论）
- nickname 客户端提供（Pydantic 校验非空、≤50 字符），v0 不做用户系统

fixtures (client / db_engine / db_session) 由 conftest.py 提供。
"""
from fastapi.testclient import TestClient


# ---------- F-2.6 POST /api/posts/{id}/comments ----------

def test_create_comment_returns_201_with_id_and_fields(client: TestClient):
    """创建评论应返回 201 + id + 必填字段"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()

    response = client.post(
        f"/api/posts/{post['id']}/comments",
        json={"nickname": "alice", "content": "写得不错"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] >= 1
    assert data["post_id"] == post["id"]
    assert data["nickname"] == "alice"
    assert data["content"] == "写得不错"


def test_create_comment_with_empty_content_returns_422(client: TestClient):
    """空 content 应被 Pydantic 拦截，返回 422"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()
    response = client.post(
        f"/api/posts/{post['id']}/comments",
        json={"nickname": "alice", "content": ""},
    )
    assert response.status_code == 422


def test_create_comment_with_empty_nickname_returns_422(client: TestClient):
    """空 nickname 应被 Pydantic 拦截，返回 422"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()
    response = client.post(
        f"/api/posts/{post['id']}/comments",
        json={"nickname": "", "content": "x"},
    )
    assert response.status_code == 422


def test_create_comment_on_nonexistent_post_returns_404(client: TestClient):
    """对不存在的 post_id 评论应返回 404"""
    response = client.post(
        "/api/posts/9999/comments",
        json={"nickname": "alice", "content": "x"},
    )
    assert response.status_code == 404


# ---------- F-2.9 DELETE /api/comments/{id} ----------

def test_delete_comment_returns_204_and_subsequent_create_still_works(client: TestClient):
    """删评论 204；删后再发一条新评论应能正常创建（不报错、内容正确）"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()
    c1 = client.post(
        f"/api/posts/{post['id']}/comments",
        json={"nickname": "alice", "content": "1"},
    ).json()
    assert c1["id"] >= 1

    response = client.delete(f"/api/comments/{c1['id']}")
    assert response.status_code == 204

    # 再创建一条新评论，应能成功且内容正确
    # （SQLite :memory: AUTOINCREMENT 复用旧 id 是已知行为，不验证 id 不等）
    c2 = client.post(
        f"/api/posts/{post['id']}/comments",
        json={"nickname": "bob", "content": "2"},
    )
    assert c2.status_code == 201
    data = c2.json()
    assert data["nickname"] == "bob"
    assert data["content"] == "2"


def test_delete_nonexistent_comment_returns_404(client: TestClient):
    """删不存在的评论 id 应返回 404"""
    response = client.delete("/api/comments/9999")
    assert response.status_code == 404


def test_delete_post_cascades_to_its_comments(client: TestClient):
    """删博客应级联删它的评论（Design-Brief: ON DELETE CASCADE）"""
    post = client.post("/api/posts", json={"title": "x", "content": "y"}).json()
    c1 = client.post(
        f"/api/posts/{post['id']}/comments",
        json={"nickname": "alice", "content": "1"},
    ).json()

    # 删博客
    assert client.delete(f"/api/posts/{post['id']}").status_code == 204

    # 删过的博客下面的评论也应被级联删掉
    assert client.delete(f"/api/comments/{c1['id']}").status_code == 404