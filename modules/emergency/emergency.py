import streamlit as st

translations = {
    "es": {
        "title": "Módulo de Emergencias",
        "welcome": "Bienvenido al Módulo de Emergencias. Aquí puedes gestionar casos de emergencia y admisiones de pacientes.",
        "coming": "Funcionalidad Próximamente",
        "desc": "Este módulo incluirá funciones como registrar casos de emergencia, gestionar admisiones y rastrear el estado de la sala de emergencias."
    },
    "en": {
        "title": "Emergency Module",
        "welcome": "Welcome to the Emergency Module. Here, you can manage emergency cases and patient admissions.",
        "coming": "Functionality Coming Soon",
        "desc": "This module will include features such as recording emergency cases, managing patient admissions, and tracking emergency room status."
    }
}

def t(key):
    lang = st.session_state.get("language", "en")
    return translations[lang].get(key, key)

def emergency_page():
    st.title(t("title"))
    st.write(t("welcome"))
    st.subheader(t("coming"))
    st.write(t("desc"))
    
    # Añadir cualquier funcionalidad futura aquí
