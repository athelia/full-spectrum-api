import pytest
from model import app

@pytest.fixture()
def client():
    app.config.update({
        "TESTING": True,
    })
    return app.test_client()

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert f"welcome to full spectrum eggs" in response.data

def test_foo():
    assert 2 + 2 == 4