import streamlit as st
import requests
 
BASE_URL = "http://127.0.0.1:8000"
 
 
def get_all_notes():
    response = requests.get(f"{BASE_URL}/notes")
    if response.status_code == 200:
        return response.json()
    return []
 
 
def create_note(title, content, category, tags):
    payload = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
    }
    response = requests.post(f"{BASE_URL}/notes", json=payload)
    return response
 
 
# ─── Seitentitel ────────────────────────────────────────────────────────────
 
st.title("📝 Notes App")
 
# ─── Tab-Layout ─────────────────────────────────────────────────────────────
 
tab1, tab2 = st.tabs(["📋 Notizen anzeigen", "➕ Neue Notiz erstellen"])
 
 
with tab1:
    st.subheader("Alle Notizen")
 
    if st.button("🔄 Aktualisieren"):
        st.rerun()
 
    notes = get_all_notes()
 
    if not notes:
        st.info("Noch keine Notizen vorhanden.")
    else:
        # Titel-Liste als Auswahlmenü
        titles = [f"{note['id']} – {note['title']}" for note in notes]
        selected = st.selectbox("Notiz auswählen", titles)
 
        # Passende Notiz heraussuchen
        selected_id = int(selected.split("–")[0].strip())
        note = next(n for n in notes if n["id"] == selected_id)
 
        # Details anzeigen
        st.markdown("---")
        st.markdown(f"### {note['title']}")
        st.markdown(f"**Kategorie:** {note['category']}")
        st.markdown(f"**Tags:** {', '.join(note['tags']) if note['tags'] else '–'}")
        st.markdown(f"**Erstellt am:** {note['created_at'][:10]}")
        st.markdown("**Inhalt:**")
        st.write(note["content"])
 
 
with tab2:
    st.subheader("Neue Notiz erstellen")
 
    with st.form("create_note_form"):
        title = st.text_input("Titel *", placeholder="z. B. Einkaufsliste")
        content = st.text_area("Inhalt *", placeholder="Was möchtest du festhalten?")
        category = st.text_input("Kategorie *", placeholder="z. B. work, personal, school")
        tags_input = st.text_input("Tags (kommagetrennt)", placeholder="z. B. urgent, todo")
 
        submitted = st.form_submit_button("✅ Notiz speichern")
 
    if submitted:
        # Eingaben validieren
        if not title or not content or not category:
            st.error("Bitte Titel, Inhalt und Kategorie ausfüllen.")
        else:
            tags = [t.strip() for t in tags_input.split(",") if t.strip()]
            response = create_note(title, content, category, tags)
 
            if response.status_code == 201:
                st.success(f"Notiz '{title}' erfolgreich erstellt!")
                st.balloons()
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                st.error(f"Fehler: {detail}")
