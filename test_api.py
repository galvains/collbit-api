import httpx

from fastapi.testclient import TestClient
from main import app

# client = TestClient(app)
client = httpx.Client()
ENDPOINT = "http://localhost:8000"


def test_home():
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello, world!'}


def test_can_get_all_tickets():
    response = client.get(ENDPOINT + '/api/v1/tickets')
    assert response.status_code == 200
    assert len(response.json()) == 30
