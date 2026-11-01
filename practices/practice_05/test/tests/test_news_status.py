from fastapi.testclient import TestClient
from app.main import app, _reset_state


client = TestClient(app)


def test_news_crud_minimal():
    _reset_state()
    r = client.get("/api/v1/news/")
    assert r.status_code == 200
    # create
    r = client.post("/api/v1/news/", json={"title": "Promo", "body": "-10% today"})
    assert r.status_code == 201


def test_status_hours_and_open():
    _reset_state()
    r = client.get("/api/v1/status/hours")
    assert r.status_code == 200
    assert "open" in r.json() and "close" in r.json()
    r = client.get("/api/v1/status/open", params={"now": "21:00"})
    assert r.status_code == 200
    assert r.json()["open"] in (True, False)
