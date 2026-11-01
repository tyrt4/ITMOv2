from fastapi.testclient import TestClient
from app.main import app, _reset_state


client = TestClient(app)


def test_menu_empty_initially():
    _reset_state()
    r = client.get("/api/v1/menu/")
    assert r.status_code == 200
    assert r.json() == []


def test_menu_crud_flow():
    payload = {
        "name": "Espresso",
        "ingredients": ["coffee"],
        "sizes": ["single"],
        "priceCoffeeCoin": 3.0,
    }
    # Создание
    r = client.post("/api/v1/menu/", json=payload)
    assert r.status_code == 201
    item = r.json()
    assert item["id"] >= 1
    mid = item["id"]

    # Чтение
    r = client.get(f"/api/v1/menu/{mid}")
    assert r.status_code == 200

    # Обновление
    upd = dict(payload)
    upd["priceCoffeeCoin"] = 3.5
    r = client.put(f"/api/v1/menu/{mid}", json=upd)
    assert r.status_code == 200
    assert r.json()["priceCoffeeCoin"] == 3.5

    # Удаление
    r = client.delete(f"/api/v1/menu/{mid}")
    assert r.status_code == 204
    r = client.get(f"/api/v1/menu/{mid}")
    assert r.status_code == 404
