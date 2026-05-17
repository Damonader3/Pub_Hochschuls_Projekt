from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import json
from pathlib import Path


app = FastAPI(
    title="Applied Programming Course - Hello World Note Taking API",
    description="A simple API to demonstrate FastAPI capabilities for note taking application.",
    version="1.0.0"
)



@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/name/{name}")
def greet_name(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/square/{number}")
def calculate_square(number: float):
    """
    Takes a number and returns its square.
    """
    result = number ** 2
    return {
        "original_number": number, 
        "square": result
    }

@app.get("/student")
def get_student():
    return {
        "name": "Dominic Schifferdecker",  
        "semester": 1,              
        "course": "Wirtschaftsinformatik 2.0",
        "university": "Hoschule Coburg"    
    }

@app.get("/double/{number}")
def calculate_double(number: float):
    result = number * 2
    return {"original_number": number, "doubled": result}

####################################
# Note Taking API Endpoints
####################################

class NoteCreate(BaseModel):
    title: str
    content: str
    category: str  
    tags: list[str] = []  

class Note(BaseModel):
    id: int
    title: str
    content: str
    category: str  
    tags: list[str] = []  
    created_at: str

NOTES_FILE = Path("data/notes.json")

def load_notes():
    """Load notes from JSON file and return notes list and next ID counter"""
    notes_db = []
    note_id_counter = 1

    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:
            data = json.load(f)
            notes_db = [Note(**note) for note in data]

            # Set counter to max ID + 1
            if notes_db:
                note_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, note_id_counter


def save_notes(notes_db):
    """Save notes to JSON file after each change"""
    # Ensure data directory exists
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, 'w') as f:
        # Convert Note objects to dicts
        notes_data = [note.model_dump() if hasattr(note, "model_dump") else note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate) -> Note:
    """Create a new note with category"""
    notes_db, note_id_counter = load_notes()

    new_note = Note(
        id=note_id_counter,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=note.tags,  
        created_at=datetime.now(timezone.utc).isoformat()
    )

    notes_db.append(new_note)
    save_notes(notes_db)

    return new_note


@app.get("/notes")
def list_notes(
    category: str = None,
    search: str = None,
    tag: str = None
) -> list[Note]:
    """List notes with optional filters (category, keyword search, or tag)"""
    notes_db, _ = load_notes()
    filtered = []
    
    for note in notes_db:
        if category and note.category != category:
            continue
        if search:
            search_lower = search.lower()
            if search_lower not in note.title.lower() and search_lower not in note.content.lower():
                continue
        if tag and tag not in note.tags:
            continue
        filtered.append(note)
        
    return filtered

@app.get("/notes/stats")
def get_notes_stats():
    """Task 3: Get statistics about notes (Count total and by category)"""
    notes_db, _ = load_notes()
    
    categories = {}
    for note in notes_db:
        if note.category in categories:
            categories[note.category] += 1
        else:
            categories[note.category] = 1
    
    return {
        "total_notes": len(notes_db),
        "by_category": categories
    }

@app.get("/notes/category/{category}")
def get_notes_by_category(category: str):
    """Task 2: Get all notes in a specific category"""
    filtered_notes = []
    notes_db, _ = load_notes()

    for note in notes_db:
        if note.category == category:
            filtered_notes.append(note)
    
    return filtered_notes

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    """Get a specific note by ID"""
    notes_db, _ = load_notes()
    for note in notes_db:
        if note.id == note_id:
            return note
    
    # Not found - raise 404 error
    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )

@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate) -> Note:
    """Update an existing note while maintaining its ID and timestamp"""
    notes_db, _ = load_notes()
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            updated_note = Note(
                id=note.id,
                title=note_update.title,
                content=note_update.content,
                category=note_update.category,
                tags=note_update.tags,
                created_at=note.created_at
            )
            notes_db[i] = updated_note
            save_notes(notes_db)
            return updated_note
    raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

@app.get("/tags")
def list_tags() -> list[str]:
    """Get all unique tags across all stored notes"""
    notes_db, _ = load_notes()
    all_tags = set()
    for note in notes_db:
        for tag in note.tags:
            all_tags.add(tag)
    return sorted(list(all_tags))

@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str) -> list[Note]:
    """Get sub-collection of all notes assigned to a specific tag resource"""
    notes_db, _ = load_notes()
    return [note for note in notes_db if tag_name in note.tags]

@app.delete("/notes/{note_id}", status_code=204)  
def delete_note(note_id: int):
    """Bonus Challenge: Delete a note by ID"""
    notes_db, _ = load_notes()
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i)
            save_notes(notes_db)
            return  
    
    raise HTTPException(status_code=404, detail="Note not found")