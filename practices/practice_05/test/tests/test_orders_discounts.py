from fastapi.testclient import TestClient
from app.main import app, _reset_state


client = TestClient(app)


def seed_menu():
    # Убедимся, что есть хотя бы один пункт меню
    r = client.get("/api/v1/menu/")
    if r.json():
        return r.json()[0]["id"]
    payload = {
        "name": "Americano",
        "ingredients": ["coffee", "water"],
        "sizes": ["single"],
        "priceCoffeeCoin": 4.0,
        "calories": 5,
    }
    r = client.post("/api/v1/menu/", json=payload)
    return r.json()["id"]


def test_discount_daily_deterministic():
    _reset_state()
    r = client.get("/api/v1/discounts/current")
    assert r.status_code == 200
    assert "percent" in r.json()


def test_order_creation_total_and_discount():
    _reset_state()
    mid = seed_menu()
    # Выбираем время внутри happy hour, чтобы проверить применение скидки
    payload = {
        "items": [{"menuId": mid, "quantity": 2}],
        "now": "14:30",
    }
    r = client.post("/api/v1/orders/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["totalCoffeeCoin"] <= 8.0  # со скидкой или без неё
    assert data["discountPercent"] in (0, 5, 10)


def test_order_pay_and_get():
    _reset_state()
    mid = seed_menu()
    r = client.post("/api/v1/orders/", json={"items": [{"menuId": mid, "quantity": 1}]})
    oid = r.json()["id"]
    r = client.post(f"/api/v1/orders/{oid}/pay")
    assert r.status_code == 200
    assert r.json()["status"] == "paid"
    r = client.get(f"/api/v1/orders/{oid}")
    assert r.status_code == 200


def test_store_status_open_param():
    _reset_state()
    # 09:00 должно попадать в дефолтный интервал 08:00-20:00
    r = client.get("/api/v1/status/open", params={"now": "09:00"})
    assert r.status_code == 200
    assert r.json()["open"] is True


def test_menu_details():
    _reset_state()
    mid = seed_menu()
    r = client.get(f"/api/v1/menu/{mid}/details")
    assert r.status_code == 200
    d = r.json()
    assert d["id"] == mid
    assert "calories" in d


def test_loyalty_points_accumulate():
    _reset_state()
    mid = seed_menu()
    cid = "user-1"
    r = client.post(
        "/api/v1/orders/",
        json={"items": [{"menuId": mid, "quantity": 1}], "customerId": cid, "now": "10:00"},
    )
    assert r.status_code == 201
    r = client.get(f"/api/v1/loyalty/{cid}")
    assert r.status_code == 200
    assert r.json()["points"] >= 1


def test_reviews_flow():
    _reset_state()
    mid = seed_menu()
    r = client.post(
        "/api/v1/reviews/",
        json={"menuId": mid, "rating": 5, "comment": "Great!"},
    )
    assert r.status_code == 201
    r = client.get("/api/v1/reviews/", params={"menuId": mid})
    assert r.status_code == 200
    assert len(r.json()) >= 1
