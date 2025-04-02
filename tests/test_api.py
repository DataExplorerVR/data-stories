import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Data Stories API"}

def test_get_monthly_sinkings():
    # Test without parameters (full dataset)
    response = client.get("/api/sinkings/monthly")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0  # Should have data
    
    # Test 1942 data
    response = client.get("/api/sinkings/monthly?start_date=1942-01-01&end_date=1942-12-31")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 3  # Three months in test data (Jan, Feb, Mar)
    
    # Test December 1941 specifically
    response = client.get("/api/sinkings/monthly?start_date=1941-12-01&end_date=1941-12-31")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    dec_1941 = data["data"][0]
    assert dec_1941["total_sinkings"] == 3  # 3 ships in test data
    assert dec_1941["total_tonnage"] == 45800.0  # Sum of tonnage in test data
    
    # Test invalid date format
    response = client.get("/api/sinkings/monthly?start_date=invalid")
    assert response.status_code == 422  # FastAPI validation error
