import requests
import json
from jsonschema import validate

BASE_URL = "http://localhost:8000"

# Load schema.json
with open("schema.json") as f:
    schema = json.load(f)

def test_health():
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
    print("✅ /health test passed")

def test_version():
    res = requests.get(f"{BASE_URL}/version")
    assert res.status_code == 200
    assert "model_name" in res.json()
    assert "version" in res.json()
    print("✅ /version test passed")

def test_predict_spam():
    res = requests.post(f"{BASE_URL}/predict", json={"post": "Win a free recharge now!"})
    assert res.status_code == 200
    data = res.json()

    # Check response fields
    assert "label" in data
    assert "confidence" in data

    # Validate against schema
    validate(instance=data, schema=schema)#["output"])
    print("✅ Spam prediction test passed & matches schema")

def test_predict_empty():
    res = requests.post(f"{BASE_URL}/predict", json={"post": ""})
    assert res.status_code == 400
    print("✅ Empty input test passed")

if __name__ == "__main__":
    test_health()
    test_version()
    test_predict_spam()
    test_predict_empty()