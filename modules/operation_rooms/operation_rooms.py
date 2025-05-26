import streamlit as st

translations = {
    "es": {
        "title": "Módulo de Quirófanos",
        "welcome": "Bienvenido al Módulo de Quirófanos. Aquí puedes gestionar horarios de cirugía, asignación de salas y monitorear el estado de operaciones.",
        "coming": "Funcionalidad Próximamente",
        "desc": "Este módulo incluirá funciones como agendar cirugías, asignar quirófanos y rastrear el estado de las operaciones."
    },
    "en": {
        "title": "Operating Rooms Module",
        "welcome": "Welcome to the Operating Rooms Module. Here, you can manage surgery schedules, room assignments, and monitor operation status.",
        "coming": "Functionality Coming Soon",
        "desc": "This module will include features such as scheduling surgeries, assigning operating rooms, and tracking the status of operations."
    }
}

def t(key):
    lang = st.session_state.get("language", "en")
    return translations[lang].get(key, key)

def operating_rooms_page():
    st.title(t("title"))
    st.write(t("welcome"))
    
    st.subheader(t("coming"))
    st.write(t("desc"))
    
    # Añadir cualquier funcionalidad futura aquí
