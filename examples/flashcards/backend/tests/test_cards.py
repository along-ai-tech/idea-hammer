def test_create_card_persists_and_returns_id(client):
    """创建卡片返回带 id 的完整记录，证明数据已持久化"""
    payload = {"front": "LangGraph StateGraph", "back": "状态图节点容器"}
    response = client.post("/api/cards", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["front"] == "LangGraph StateGraph"
    assert data["back"] == "状态图节点容器"
    assert isinstance(data["id"], int)


def test_list_cards_returns_empty_array_initially(client):
    """空库返回空数组而非 None，证明接口契约稳定"""
    response = client.get("/api/cards")
    assert response.status_code == 200
    assert response.json() == []


def test_list_cards_returns_created_card(client):
    """创建的卡片能在列表里找到，证明 GET 与 POST 走同一持久层"""
    created = client.post("/api/cards", json={"front": "A", "back": "B"}).json()
    response = client.get("/api/cards")
    assert response.status_code == 200
    cards = response.json()
    assert len(cards) == 1
    assert cards[0]["front"] == "A"
    assert cards[0]["back"] == "B"
    assert cards[0]["id"] == created["id"]


def test_get_card_by_id_returns_stored_card(client):
    """按 id 查卡片返回存储的内容"""
    created = client.post("/api/cards", json={"front": "Q", "back": "A"}).json()
    response = client.get(f"/api/cards/{created['id']}")
    assert response.status_code == 200
    assert response.json()["front"] == "Q"


def test_get_nonexistent_card_returns_404(client):
    """查不存在的卡片返回 404 而非 None 或 500"""
    response = client.get("/api/cards/9999")
    assert response.status_code == 404


def test_update_card_modifies_persisted_fields(client):
    """更新卡片字段会持久化，再次 GET 能拿到新内容"""
    created = client.post("/api/cards", json={"front": "old", "back": "old"}).json()
    update_resp = client.put(
        f"/api/cards/{created['id']}",
        json={"front": "new front", "back": "new back"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["front"] == "new front"
    get_resp = client.get(f"/api/cards/{created['id']}")
    assert get_resp.json()["front"] == "new front"
    assert get_resp.json()["back"] == "new back"


def test_delete_card_makes_subsequent_get_return_404(client):
    """删除后 GET 应 404，证明删除生效而非软删除"""
    created = client.post("/api/cards", json={"front": "x", "back": "y"}).json()
    delete_resp = client.delete(f"/api/cards/{created['id']}")
    assert delete_resp.status_code == 204
    assert client.get(f"/api/cards/{created['id']}").status_code == 404


def test_update_nonexistent_card_returns_404(client):
    """更新不存在的卡片返回 404"""
    response = client.put("/api/cards/9999", json={"front": "x", "back": "y"})
    assert response.status_code == 404


def test_delete_nonexistent_card_returns_404(client):
    """删除不存在的卡片返回 404"""
    response = client.delete("/api/cards/9999")
    assert response.status_code == 404
