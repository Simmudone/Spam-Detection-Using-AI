import requests

BASE_URL = "http://localhost:8000"

def test_empty_string():
    response = requests.post(f"{BASE_URL}/predict", json={"post": ""})
    assert response.status_code == 400
    print("✅ Empty string test passed")

def test_only_emojis():
    response = requests.post(f"{BASE_URL}/predict", json={"post": "🔥🔥🔥😂😂"})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "confidence" in data
    print("✅ Emoji input test passed")

def test_only_numbers():
    response = requests.post(f"{BASE_URL}/predict", json={"post": "1234567890"})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    print("✅ Numbers-only input test passed")

def test_long_text():
    long_message = "win free " * 200  # repeated to simulate spammy long input
    response = requests.post(f"{BASE_URL}/predict", json={"post": long_message})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    print("✅ Long spammy input test passed")

if __name__ == "__main__":
    test_empty_string()
    test_only_emojis()
    test_only_numbers()
    test_long_text()
