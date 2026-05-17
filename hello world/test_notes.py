import requests
import pytest


BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Diese Hilfsfunktion läuft automatisch vor JEDEM einzelnen Test.
    Sie löscht alle alten Notizen, damit jeder Test bei Null anfängt.
    """
    response = requests.get(f"{BASE_URL}/notes")
    if response.status_code == 200:
        notes = response.json()
        # Jede gefundene Note löschen
        for note in notes:
            requests.delete(f"{BASE_URL}/notes/{note['id']}")


def test_create_note():
    """Testet das erfolgreiche Erstellen einer Notiz (HTTP 201)"""
    payload = {
        "title": "Test Note",
        "content": "This is a test",
        "category": "Work",
        "tags": ["pytest", "test"]
    }
    response = requests.post(f"{BASE_URL}/notes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data
    assert "created_at" in data

def test_list_notes():
    """Testet das Abrufen der Notizen-Liste"""
    payload = {"title": "List Test", "content": "Checking list", "category": "Uni", "tags": []}
    requests.post(f"{BASE_URL}/notes", json=payload)
    
    response = requests.get(f"{BASE_URL}/notes")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_note_by_id():
    """Testet das Abrufen einer spezifischen Notiz über ihre ID"""
    payload = {"title": "ID Test", "content": "Find me", "category": "Personal", "tags": []}
    created_note = requests.post(f"{BASE_URL}/notes", json=payload).json()
    note_id = created_note["id"]
    
    response = requests.get(f"{BASE_URL}/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "ID Test"

def test_update_note():
    """Testet das Aktualisieren einer Notiz via PUT"""
    payload = {"title": "Old Title", "content": "Old content", "category": "Work", "tags": []}
    created_note = requests.post(f"{BASE_URL}/notes", json=payload).json()
    note_id = created_note["id"]
    
    update_payload = {"title": "New Title", "content": "Updated content", "category": "Work", "tags": ["updated"]}
    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=update_payload)
    
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert "updated" in response.json()["tags"]

def test_delete_note():
    """Testet das Löschen einer Notiz (HTTP 204 No Content)"""
    payload = {"title": "To Delete", "content": "Bye bye", "category": "Trash", "tags": []}
    created_note = requests.post(f"{BASE_URL}/notes", json=payload).json()
    note_id = created_note["id"]
    
    response = requests.delete(f"{BASE_URL}/notes/{note_id}")
    assert response.status_code == 204


def test_filter_by_category():
    """Testet den Query-Filter nach Kategorie"""
    requests.post(f"{BASE_URL}/notes", json={"title": "A", "content": "X", "category": "Work", "tags": []})
    requests.post(f"{BASE_URL}/notes", json={"title": "B", "content": "Y", "category": "Uni", "tags": []})
    
    response = requests.get(f"{BASE_URL}/notes?category=Work")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "Work"

def test_filter_by_search():
    """Testet die Stichwortsuche (case-insensitive)"""
    requests.post(f"{BASE_URL}/notes", json={"title": "Kaffee trinken", "content": "Wichtig", "category": "Break", "tags": []})
    requests.post(f"{BASE_URL}/notes", json={"title": "FastAPI lernen", "content": "Code schreiben", "category": "Coding", "tags": []})
    
    response = requests.get(f"{BASE_URL}/notes?search=fastapi")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert "FastAPI" in response.json()[0]["title"]

def test_filter_by_tag():
    """Testet das Filtern nach einem bestimmten Tag"""
    requests.post(f"{BASE_URL}/notes", json={"title": "A", "content": "X", "category": "A", "tags": ["important"]})
    requests.post(f"{BASE_URL}/notes", json={"title": "B", "content": "Y", "category": "B", "tags": ["archived"]})
    
    response = requests.get(f"{BASE_URL}/notes?tag=important")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_combined_filters():
    """Testet die Kombination mehrerer Filter (Kategorie + Suche)"""
    requests.post(f"{BASE_URL}/notes", json={"title": "FastAPI Setup", "content": "Text", "category": "Uni", "tags": []})
    requests.post(f"{BASE_URL}/notes", json={"title": "FastAPI Project", "content": "Text", "category": "Work", "tags": []})
    
    response = requests.get(f"{BASE_URL}/notes?category=Work&search=FastAPI")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "Work"


def test_create_note_missing_field():
    """Testet die automatische Pydantic-Validierung bei fehlenden Feldern (HTTP 422)"""
    incomplete_payload = {"title": "Missing fields"} # Es fehlen content, category und tags
    response = requests.post(f"{BASE_URL}/notes", json=incomplete_payload)
    assert response.status_code == 422

def test_get_nonexistent_note():
    """Testet den Fehlerfall beim Abrufen einer nicht existierenden ID (HTTP 404)"""
    response = requests.get(f"{BASE_URL}/notes/99999")
    assert response.status_code == 404

def test_update_nonexistent_note():
    """Testet den Fehlerfall beim Aktualisieren einer nicht existierenden ID (HTTP 404)"""
    payload = {"title": "Ghost", "content": "Ghost", "category": "Ghost", "tags": []}
    response = requests.put(f"{BASE_URL}/notes/99999", json=payload)
    assert response.status_code == 404

def test_delete_nonexistent_note():
    """Testet den Fehlerfall beim Löschen einer nicht existierenden ID (HTTP 404)"""
    response = requests.delete(f"{BASE_URL}/notes/99999")
    assert response.status_code == 404


def test_notes_statistics():
    """Testet den Statistik-Endpunkt aus Tag 3"""
    requests.post(f"{BASE_URL}/notes", json={"title": "A", "content": "X", "category": "Work", "tags": []})
    requests.post(f"{BASE_URL}/notes", json={"title": "B", "content": "Y", "category": "Work", "tags": []})
    requests.post(f"{BASE_URL}/notes", json={"title": "C", "content": "Z", "category": "Uni", "tags": []})
    
    response = requests.get(f"{BASE_URL}/notes/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_notes"] == 3
    assert stats["by_category"]["Work"] == 2
    assert stats["by_category"]["Uni"] == 1

def test_get_notes_by_category_path():
    """Testet den dedizierten Kategorie-Pfad-Endpunkt (/notes/category/{category})"""
    requests.post(f"{BASE_URL}/notes", json={"title": "Note", "content": "Content", "category": "Private", "tags": []})
    
    response = requests.get(f"{BASE_URL}/notes/category/Private")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "Private"