import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.mark.benchmark(group="menu")
def test_bench_get_menu(benchmark):
    def get_menu():
        r = client.get("/api/v1/menu/")
        assert r.status_code == 200
        return r.json()

    result = benchmark(get_menu)
    assert isinstance(result, list)


@pytest.mark.benchmark(group="discount")
def test_bench_discount(benchmark):
    def get_discount():
        r = client.get("/api/v1/discounts/current")
        assert r.status_code == 200
        return r.json()

    result = benchmark(get_discount)
    assert "percent" in result


@pytest.mark.benchmark(group="order")
def test_bench_create_order(benchmark):
    # Убедимся, что есть хотя бы один пункт меню
    r = client.get("/api/v1/menu/")
    if not r.json():
        client.post(
            "/api/v1/menu/",
            json={
                "name": "Bench",
                "ingredients": [],
                "sizes": [],
                "priceCoffeeCoin": 1.0,
                "calories": 0,
            },
        )
        r = client.get("/api/v1/menu/")
    mid = r.json()[0]["id"]

    def create_order():
        r = client.post(
            "/api/v1/orders/",
            json={"items": [{"menuId": mid, "quantity": 1}], "now": "10:00"},
        )
        assert r.status_code == 201
        return r.json()

    result = benchmark(create_order)
    assert result["id"] >= 1
