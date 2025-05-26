import streamlit as st

translations = {
    "es": {
        "title": "Módulo de Hospitalización",
        "welcome": "Bienvenido al Módulo de Hospitalización. Aquí puedes gestionar ingresos, asignación de camas y altas de pacientes.",
        "coming": "Funcionalidad Próximamente",
        "desc": "Este módulo incluirá funciones como registrar ingresos, gestionar camas y procesar altas."
    },
    "en": {
        "title": "Hospitalization Module",
        "welcome": "Welcome to the Hospitalization Module. Here, you can manage patient admissions, bed assignments, and discharge processes.",
        "coming": "Functionality Coming Soon",
        "desc": "This module will include features such as recording patient admissions, managing bed assignments, and processing discharges."
    }
}

def t(key):
    lang = st.session_state.get("language", "en")
    return translations[lang].get(key, key)

def hospitalization_page():
    st.title(t("title"))
    st.write(t("welcome"))
    st.subheader(t("coming"))
    st.write(t("desc"))
    
    # Añadir cualquier funcionalidad futura aquí
