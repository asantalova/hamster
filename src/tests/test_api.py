import requests
import pytest

BASE_URL = 'https://reqres.in/api'

@pytest.mark.xray(test_key="TPT-74")
def test_create_user():
    payload = {
        "name": "Happy Hamster",
        "job" : "Family member"
    }

    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201

    response_data = response.json()
    assert response_data["name"] == payload["name"]
    assert response_data["job"] == payload["job"]
    assert "id" in response_data
    assert "createdAt" in response_data