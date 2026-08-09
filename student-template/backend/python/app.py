import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_alerts_route(client, monkeypatch):
    # Mock the database connection and cursor to isolate the test
    class MockCursor:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def execute(self, query):
            pass
        def fetchall(self):
            return [{"id": 1, "name": "Item A", "quantity": 5, "reorder_level": 10, "sku": "SKU123"}]

    class MockConn:
        def cursor(self, cursor_factory=None):
            return MockCursor()
        def close(self):
            pass

    monkeypatch.setattr("app.get_db_connection", lambda: MockConn())

    response = client.get('/api/inventory/alerts')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Item A"
