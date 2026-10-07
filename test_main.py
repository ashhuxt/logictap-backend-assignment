import pytest
from fastapi.testclient import TestClient
from main import app, calls_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    calls_db.clear()

def test_duplicate_call_ended_does_not_create_second_record():
    payload = {"call_id": "abc123", "status": "answered", "duration_secs": 42}
    
    # Initial POST request
    res1 = client.post("/call-ended", json=payload)
    assert res1.status_code == 200
    assert len(calls_db) == 1
    
    # Duplicate POST request
    res2 = client.post("/call-ended", json=payload)
    assert res2.status_code == 200
    assert len(calls_db) == 1  # Ensures record count remains 1
