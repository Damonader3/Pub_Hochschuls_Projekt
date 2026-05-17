# Work Log

**Student Name:** 

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

## Template:

---

## 1. ✅ What did I accomplish?

_Reflect on the activities, exercises, and work you completed today._

**Guiding questions:**
- What topics or concepts did you work with?
- What exercises or projects did you complete?
- What tools or technologies did you use?
- What did you learn or practice?



---

## 2. 🚧 What challenges did I face?

_Describe any difficulties, obstacles, or confusing moments you encountered._

**Guiding questions:**
- What was difficult to understand?
- Where did you get stuck?
- What errors or problems did you face?
- What felt frustrating or confusing?




---

## 3. 💡 How did I overcome them?

_Explain how you overcame the challenges or what help you needed._

**Guiding questions:**
- What strategies did you try?
- Who or what helped you (instructor, classmates, documentation)?
- What did you learn from solving the problem?
- What questions do you still have?


---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?
- Set up von einer FastAPI mit "uv" package manager mit dem command uv run fastapi dev.
- Erste Projekte: /square /students /double etc.
- Erste Übungen mit Swagger im Browser und erfolgreiche JSON responses.

---

#### 2. 🚧 What challenges did I face?
- ERROR: (Path does not exist main.py) weil meine main.py datei in einem subdirectory ist (hello world).
- ERROR: (Command syntax issues) Subfolder name hat ein lerzeichen.
- Swagger UI war am anfang verwirrend. (Response Codes etc.)

---

#### 3. 💡 How did I overcome them?
- Uv run cmd mit genaueren angaben ausgeführt => (uv run hello world/main.py).
- Habe als hilfe AI genutzt, um mir meine Fehler erklären zu lassen.
- Habe andere Githubs/Communities als Beispiele benutzt um meine Fehler selbst zu korrigieren

---

### Day 2

#### 1. ✅ What did I accomplish?
- Erste Note Taking API
- Bonus Challange!
- Erweiterung der API Endpunkte (Homework)
- Error Handling gemeistert (HTTPException 404 und 500)
- Daten Grupierungen Erstellt

---

#### 2. 🚧 What challenges did I face?
- Erneute Probleme mit Directory Path Mismatches.
- 500 Internal Server Errors
- "Legacy" Daten Konflikte
- CLI Syntax Error
- Strenges Schema Rigidit

---

#### 3. 💡 How did I overcome them?
- Nach Recherche den Command "cd "hello world" benutzt
- Datenbasis resetet um Error Code 500 zu beheben und "Legacy" Daten Konflikte (notes.json gelöscht)
- Log Analysen und gezielte suche nach Fehlercodes im Internet
- UI Neustart um alle Endpunkte neuzustarten





---

### Day 3

#### 1. ✅ What did I accomplish?
- Hinzufügen von REST-konformen Put- und DElete-Endpunkten
- Tag-Arrays integriert: Die Dtenmodelle (Note und NoteCreate) erweotert ,ot tags (tags: list[str] = [])
- Komplexe Filterlogik entwickelt: Der Endpunkt GET /notes wurde komplett überarbeitet
- Durch die erstellung von /tags und /tags{tag_names}/notes habe ich ein REST-Designmuster etabliert um Tags als eigenständige, auffindbare Sammlung bereitzustellen

---

#### 2. 🚧 What challenges did I face?
- JSON- Syntax- und Decode-Fehler: Bei API-Aufrufen über die UI traten 422 Unprocessable Content -Fehler auf, durch einen Formatierungsfehler
- Interner Server-Fehler durch Dateikonflikte: Es kam ernaut zu 500 Internal Server Error durch notes.json
- Veraltete UTC angabe hat zu Server Crashes geführt

---

#### 3. 💡 How did I overcome them?
- Ein sauberer Server-Restart mit gelöschter notes.json hat den Fehlercode 500 beseitigt
- JSON Formatierung beachtet (Bei tags [food] eingegeben und nicht ["food"]. " muss mit)
- Eingebautes Copilot benutzt um den UTC fehler zu beheben

---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?
- Automatisierte Test-Code aufgebaut, welche die API-Funktionalität überprüft
- Nach anwendung des pytests waren 15 von 15 erfolgreich
- 




---

#### 2. 🚧 What challenges did I face?
- Leere Testdatei (0 KB)
- Pfad- und Verzeichnis- Verwirrung da der test main.py gefunden hat, aber nicht drauf zugreifen konnte
- Gleichzeitiges Server- und Testmanagment

---

#### 3. 💡 How did I overcome them?
- Leere Testdatei wurde behoben durch Speichern. => Speicher ist immer zum Vorteil
- Erneute Probleme durch den Order name "hello world" weshalb ich den ordner "helloworld" umbenannt habe
- test_notes.py konnte auf main.py zugreifen, nachdem beide im selben subfolder eingeordnet waren

---

### Day 5

#### 1. ✅ What did I accomplish?
- Alle 15 Tests ergebnisse erflogreich mit Passed abgeschlossen (test_notes.py)
- Validierungs Korrigiert: Den field-validator("category") so umgeschrieben, dass er weiterhin die Gültigkeit prüft 
- Alle 8 Tests waren erfolgreich (test_validation.py)
- Alle Endpunkte erfolgreich ausgeweitet

---

#### 2. 🚧 What challenges did I face?
- Nach den ersten Updates waren 9 von 15 tests Failed
- Nach auswertung der Codes konnte ich es nur auf 3 veringern
- Der Basiscode hat den API immer zum Crashen gebracht (z. 70)
- Erstellung der test_validation.py
- Verfälschte Ergebnisse durch eine Veraltete notes.json datei
- Fehler da die API im Hintergrund Kategorien als "work" speicherte und die Test-Suite "Work" gesucht hat

---

#### 3. 💡 How did I overcome them?
- Die letzten 3 Filed test habe ich mit hilfe von Gemini gelöst. => Einrückungsfehler in Zeile 70 hat die API Abstürzen lassen und war schuld für 3 Fehlerhafte Tests
- Code erweitert bzw. auf das Level grbacht damit alle endpunkte mit der Erweiterung zurecht kommen
- Erstellung der test_validation.py mit hilfe von Gemini, welche meine Fragen beantwortet hat mit Beispielen zur Erklärung 
- Veraltete notes.json datei gelöscht
- @field_validator("category") so umgeschrieben, dass er weiterhin die Gültigkeitprüft, am Ende aber den Original-Wert (return value) züruckgibt. Damit waren Groß- und Kleinschreibung keine Problem mehr

---

### Day 6

#### 1. ✅ What did I accomplish?
- 70 pytests-Test für eome FastAPI Notes- API zum Laufen gebracht
- Fehlende Endpoints implementiert: PATCH /notes/{id}, GET /categories, GET /categories/{cat}/notes
- /notes/stats um die Felder top_tags und unique_tags_count erweitert
- Datums-Filter (created_after, created_before) in GET eingebaut
- Tag-Validierung ergänzt /min. 2 Zeichen, max 10 Tags pro Note

---

#### 2. 🚧 What challenges did I face?
- Viele Tests schlugen fehl (27 von 70)
- Mehrere Endpoints fehlten komplett in der main.py
- Die Tag- Validierung war unveolständig
- Die Kategorier-Allowlist hat valide Test-Kategorien blockiert
- Der PATCH-Endpoint fehlte komplett

---

#### 3. 💡 How did I overcome them?
- Die Fehler systematisch analysiert und mit der Testdatei verglichen
- Mit Hilfe von Gemini die fehlenden Endpoints und Validierungen identifiziert und erklärt bekommen
- Jeden Fix einzeln nachvollzogen, um zu verstehen warum er nötig war
- Gelernt, dass Tests als Spezifikation gelesen werden können

---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 8

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 9

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---


# 🎉 Congratulations! You did it! 🎓✨













