from unittest.mock import MagicMock, patch

import pytest

from src.database.models import User
from src.services.auth import auth_service

@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_create_contact(client, token):
    contact_data = {"name": "Test", 
                    "surname": "Contact", 
                    "email": "test@example.com",
                    "phone": "+380971234567",
                    "birthday": "1990-05-15"}

    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None

        response = client.post(
            "/api/contacts/", 
            json=contact_data, 
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Test"
    assert "id" in data

def test_read_contacts(client, token):
    with patch.object(auth_service,  'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/", 
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["name"] == "Test"
        assert "id" in data[0]

def test_read_contact_existing(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(f"/api/contacts/1", 
                              headers={"Authorization": f"Bearer {token}"}
                              )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test"
    assert "id" in data

def test_read_contact_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

def test_update_contact_existing(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(f"/api/contacts/1", 
                              json={"surname": "New_Contact"},
                              headers={"Authorization": f"Bearer {token}"}
                              )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test"
    assert data["surname"] == "New_Contact"
    assert "id" in data

def test_update_contact_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/2",
            json={"surname": "New_Contact"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"


def test_delete_contact_existing(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(f"/api/contacts/1",
                              headers={"Authorization": f"Bearer {token}"}
                              )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test"
    assert data["surname"] == "New_Contact"
    assert "id" in data

def test_repeat_delete_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

