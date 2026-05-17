from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, ConfigDict
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


ALLOWED_CATEGORIES = {"work", "personal", "school", "ideas", "uni", "trash", "break", "coding", "a", "b", "private", "software", "ghost"}

class NoteCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    title: str = Field(min_length=1, max_length=100, description="Titel der Notiz", examples=["Einkaufsliste"])
    content: str = Field(min_length=1, description="Inhalt der Notiz")
    category: str = Field(min_length=1, max_length=30, description="Kategorie der Notiz", examples=["work"])
    tags: list[str] = Field(default_factory=list, description="Optionale Liste von Tags")

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        cleaned = value.lower()
        if cleaned not in ALLOWED_CATEGORIES:
            raise ValueError(f"Category must be one of {ALLOWED_CATEGORIES}")
        return value

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, raw_tags: list[str]) -> list[str]:
        cleaned = []
        for tag in raw_tags:
            t = tag.lower()
            if not t:
                raise ValueError("Tags cannot be empty strings")
            if t not in cleaned:
                cleaned.append(t)
        return cleaned
    
class Note(BaseModel):
    id: int
    title: str
    content: str
    category: str  
    tags: list[str] = []  
    created_at: str

NOTES_FILE = Path("data/notes.json")

def load_notes():
    notes_db = []
    note_id_counter = 1

    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:
            data = json.load(f)
            notes_db = [Note(**note) for note in data]

            if notes_db:
                note_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, note_id_counter


def save_notes(notes_db):
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, 'w') as f:
        notes_data = [note.model_dump() if hasattr(note, "model_dump") else note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate) -> Note:
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
    notes_db, _ = load_notes()
    filtered = []
    
    for note in notes_db:
        if category and note.category.lower() != category.lower():
            continue
        if search:
            search_lower = search.lower()
            if search_lower not in note.title.lower() and search_lower not in note.content.lower():
                continue
        if tag and tag.lower() not in [t.lower() for t in note.tags]:
            continue
        filtered.append(note)
        
    return filtered

@app.get("/notes/stats")
def get_notes_stats():
    notes_db, _ = load_notes()
    
    categories = {}
    for note in notes_db:
        display_cat = note.category.capitalize()
        if display_cat in categories:
            categories[display_cat] += 1
        else:
            categories[display_cat] = 1
    
    return {
        "total_notes": len(notes_db),
        "by_category": categories
    }

@app.get("/notes/category/{category}")
def get_notes_by_category(category: str):
    filtered_notes = []
    notes_db, _ = load_notes()

    for note in notes_db:
        if note.category.lower() == category.lower():
            filtered_notes.append(note)
    
    return filtered_notes

@app.get("/notes/{note_id}")
def get_note(note_id: int):
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
    notes_db, _ = load_notes()
    all_tags = set()
    for note in notes_db:
        for tag in note.tags:
            all_tags.add(tag)
    return sorted(list(all_tags))

@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str) -> list[Note]:
    notes_db, _ = load_notes()
    return [note for note in notes_db if tag_name in note.tags]

@app.delete("/notes/{note_id}", status_code=204)  
def delete_note(note_id: int):
    notes_db, _ = load_notes()
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i)
            save_notes(notes_db)
            return  
    
    raise HTTPException(status_code=404, detail="Note not found")