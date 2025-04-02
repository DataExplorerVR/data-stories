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
    assert len(data["data"]) == 45  # Known total months in dataset
    
    # Test 1942 data
    response = client.get("/api/sinkings/monthly?start_date=1942-01-01&end_date=1942-12-31")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 12  # All months in 1942
    
    # Test December 1941 specifically
    response = client.get("/api/sinkings/monthly?start_date=1941-12-01&end_date=1941-12-31")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    dec_1941 = data["data"][0]
    assert dec_1941["total_sinkings"] == 24
    assert dec_1941["total_tonnage"] == 71426.0
    
    # Test invalid date format
    response = client.get("/api/sinkings/monthly?start_date=invalid")
    assert response.status_code == 422  # FastAPI validation error
