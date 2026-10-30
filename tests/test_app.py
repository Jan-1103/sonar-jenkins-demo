from app.app import app, add, multiply


def test_add():
    assert add(2, 3) == 5


def test_multiply():
    assert multiply(2, 3) == 6


def test_home():
    r = app.test_client().get("/")
    assert r.status_code == 200


def test_health():
    r = app.test_client().get("/health")
    assert r.get_json()["status"] == "UP"


def test_add_route():
    r = app.test_client().get("/add?a=4&b=5")
    assert r.get_json()["result"] == 9


def test_multiply_route():
    r = app.test_client().get("/multiply?a=4&b=5")
    assert r.get_json()["result"] == 20
