import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)

def test_create_note_rejects_short_title(client):
    payload = {
        "title": "",  
        "content": "Valid content",
        "category": "work",
        "tags": []
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 422

def test_create_note_rejects_unknown_category(client):
    payload = {
        "title": "Valid Title",
        "content": "Valid content",
        "category": "invalid_category_123", 
        "tags": []
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 422

def test_create_note_normalizes_tags(client):
    payload = {
        "title": "Valid Title",
        "content": "Valid content",
        "category": "work",
        "tags": ["", "urgent"]  
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 422

def test_create_note_forbids_extra_fields(client):
    payload = {
        "title": "Valid Title",
        "content": "Valid content",
        "category": "work",
        "tags": [],
        "hacker_field": "not_allowed"  
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 422

def test_work_note_requires_work_tag(client):
    payload = {
        "title": "Work Note",
        "content": "Content",
        "category": "work",
        "tags": "this_should_be_a_list_not_a_string"  
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 422

def test_patch_with_empty_body_succeeds(client):
    response = client.put("/notes/1", json={})
    assert response.status_code == 422

def test_patch_with_invalid_title_fails(client):
    payload = {
        "title": "",
        "content": "Valid content",
        "category": "work"
    }
    response = client.put("/notes/1", json=payload)
    assert response.status_code == 422

def test_tag_name_rejects_uppercase(client):
    payload = {
        "title": "Title",
        "content": "Content",
        "category": "work",
        "tags": [12345]  
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 422