import streamlit as st

translations = {
    "es": {
        "title": "Módulo de UCI",
        "welcome": "Bienvenido al Módulo de UCI. Aquí puedes gestionar ingresos, asignación de camas y monitorear el estado de los pacientes en cuidados intensivos.",
        "coming": "Funcionalidad Próximamente",
        "desc": "Este módulo incluirá funciones como registrar ingresos a UCI, gestionar camas y monitorear condiciones de los pacientes."
    },
    "en": {
        "title": "ICU Module",
        "welcome": "Welcome to the ICU Module. Here, you can manage intensive care unit admissions, bed assignments, and monitor patient status.",
        "coming": "Functionality Coming Soon",
        "desc": "This module will include features such as recording ICU admissions, managing ICU bed assignments, and monitoring patient conditions."
    }
}

def t(key):
    lang = st.session_state.get("language", "en")
    return translations[lang].get(key, key)

def icu_page():
    st.title(t("title"))
    st.write(t("welcome"))
    
    st.subheader(t("coming"))
    st.write(t("desc"))
    
    # Añadir cualquier funcionalidad futura aquí
