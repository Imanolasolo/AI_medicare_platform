import streamlit as st

translations = {
    "es": {
        "title": "Módulo de Consultas",
        "welcome": "Bienvenido al Módulo de Consultas. Aquí puedes gestionar las consultas de los pacientes.",
        "coming": "Funcionalidad Próximamente",
        "desc": "Este módulo incluirá funciones como agendar citas, registrar notas de consulta y ver el historial del paciente."
    },
    "en": {
        "title": "Consultation Module",
        "welcome": "Welcome to the Consultation Module. Here, you can manage patient consultations.",
        "coming": "Functionality Coming Soon",
        "desc": "This module will include features such as scheduling appointments, recording consultation notes, and viewing patient history."
    }
}

def t(key):
    lang = st.session_state.get("language", "en")
    return translations[lang].get(key, key)

def consultation_page():
    st.title(t("title"))
    st.write(t("welcome"))
    
    st.subheader(t("coming"))
    st.write(t("desc"))
    
    # Añadir cualquier funcionalidad futura aquí
