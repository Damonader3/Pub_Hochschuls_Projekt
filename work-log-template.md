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





---

### Day 5

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 6

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






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













