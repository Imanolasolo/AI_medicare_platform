import streamlit as st

translations = {
    "es": {
        "logout": "Cerrar Sesión"
    },
    "en": {
        "logout": "Logout"
    }
}

def t(key):
    lang = st.session_state.get("language", "en")
    return translations[lang].get(key, key)

def logout_user():
    """Cierra la sesión del usuario y redirige a la página de inicio de sesión."""
    if st.button(t("logout")):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.page = 'Login'
        st.rerun()  # Refresca la aplicación para aplicar cambios
