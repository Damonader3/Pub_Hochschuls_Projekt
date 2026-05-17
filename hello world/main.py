from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime, timezone
from typing import Optional
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
    result = number ** 2
    return {"original_number": number, "square": result}


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
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    category: str = Field(min_length=1, max_length=30)
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, raw_tags: list[str]) -> list[str]:
        if len(raw_tags) > 10:
            raise ValueError("A note can have at most 10 tags")
        cleaned = []
        for tag in raw_tags:
            t = tag.strip().lower()
            if len(t) < 2:
                raise ValueError("Each tag must be at least 2 characters long")
            if t not in cleaned:
                cleaned.append(t)
        return cleaned


class NoteUpdate(BaseModel):
    """For PATCH — all fields optional."""
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    content: Optional[str] = Field(default=None, min_length=1)
    category: Optional[str] = Field(default=None, min_length=1, max_length=30)
    tags: Optional[list[str]] = None

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, raw_tags: Optional[list[str]]) -> Optional[list[str]]:
        if raw_tags is None:
            return None
        if len(raw_tags) > 10:
            raise ValueError("A note can have at most 10 tags")
        cleaned = []
        for tag in raw_tags:
            t = tag.strip().lower()
            if len(t) < 2:
                raise ValueError("Each tag must be at least 2 characters long")
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
        notes_data = [note.model_dump() for note in notes_db]
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


@app.get("/notes/stats")
def get_notes_stats():
    notes_db, _ = load_notes()

    by_category: dict[str, int] = {}
    tag_counts: dict[str, int] = {}

    for note in notes_db:
        cat = note.category
        by_category[cat] = by_category.get(cat, 0) + 1
        for tag in note.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    top_tags = [{"tag": tag, "count": count} for tag, count in sorted_tags[:5]]

    return {
        "total_notes": len(notes_db),
        "by_category": by_category,
        "top_tags": top_tags,
        "unique_tags_count": len(tag_counts),
    }


@app.get("/notes")
def list_notes(
    category: Optional[str] = None,
    search: Optional[str] = None,
    tag: Optional[str] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
) -> list[Note]:
    notes_db, _ = load_notes()
    filtered = []

    for note in notes_db:
        if category and note.category.lower() != category.lower():
            continue
        if search:
            s = search.lower()
            if s not in note.title.lower() and s not in note.content.lower():
                continue
        if tag and tag.lower() not in [t.lower() for t in note.tags]:
            continue
        if created_after or created_before:
            note_dt = datetime.fromisoformat(note.created_at)
            if created_after:
                after = created_after
                if after.tzinfo is None:
                    after = after.replace(tzinfo=timezone.utc)
                if note_dt < after:
                    continue
            if created_before:
                before = created_before
                if before.tzinfo is None:
                    before = before.replace(tzinfo=timezone.utc)
                if note_dt > before:
                    continue
        filtered.append(note)

    return filtered


@app.get("/notes/{note_id}")
def get_note(note_id: int) -> Note:
    notes_db, _ = load_notes()
    for note in notes_db:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")


@app.patch("/notes/{note_id}")
def patch_note(note_id: int, note_update: NoteUpdate) -> Note:
    notes_db, _ = load_notes()
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            updated = Note(
                id=note.id,
                title=note_update.title if note_update.title is not None else note.title,
                content=note_update.content if note_update.content is not None else note.content,
                category=note_update.category if note_update.category is not None else note.category,
                tags=note_update.tags if note_update.tags is not None else note.tags,
                created_at=note.created_at,
            )
            notes_db[i] = updated
            save_notes(notes_db)
            return updated
    raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")


@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate) -> Note:
    notes_db, _ = load_notes()
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            updated = Note(
                id=note.id,
                title=note_update.title,
                content=note_update.content,
                category=note_update.category,
                tags=note_update.tags,
                created_at=note.created_at,
            )
            notes_db[i] = updated
            save_notes(notes_db)
            return updated
    raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    notes_db, _ = load_notes()
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i)
            save_notes(notes_db)
            return
    raise HTTPException(status_code=404, detail="Note not found")


@app.get("/categories")
def list_categories() -> list[str]:
    notes_db, _ = load_notes()
    return sorted(set(note.category for note in notes_db))


@app.get("/categories/{category}/notes")
def get_notes_by_category(category: str) -> list[Note]:
    notes_db, _ = load_notes()
    return [note for note in notes_db if note.category.lower() == category.lower()]


@app.get("/tags")
def list_tags() -> list[str]:
    notes_db, _ = load_notes()
    all_tags: set[str] = set()
    for note in notes_db:
        all_tags.update(note.tags)
    return sorted(all_tags)


@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str) -> list[Note]:
    notes_db, _ = load_notes()
    name = tag_name.lower()
    return [note for note in notes_db if name in [t.lower() for t in note.tags]]