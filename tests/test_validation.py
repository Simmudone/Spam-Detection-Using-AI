import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import time
from fastapi.testclient import TestClient
from jsonschema import validate
from app.main import app

client = TestClient(app)

# Load the schema
with open("schema.json", "r") as f:
    schema = json.load(f)

# ✅ 1. Validate /predict response and response time
def test_predict_schema_and_performance():
    test_input = {"post": "Win ₹1000 cashback by clicking this link!"}
    
    start_time = time.time()
    response = client.post("/predict", json=test_input)
    duration = time.time() - start_time
    assert response.status_code == 200, "Expected 200 OK"
    
    data = response.json()
    
    # ✅ Validate against schema
    validate(instance=data, schema=schema)
    
    # ✅ Field checks
    assert data["label"] in ["spam", "not_spam"]
    assert isinstance(data["confidence"], float)
    assert 0.0 <= data["confidence"] <= 1.0
    
    # ✅ Response time check
    assert duration < 1.0, f"Response took too long: {duration:.2f}s"

# ✅ 2. Check /health endpoint
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# ✅ 3. Check /version endpoint
def test_version_info():
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "version" in data

