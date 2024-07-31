import streamlit as st

def logout_user():
    """Cierra la sesión del usuario y redirige a la página de inicio de sesión."""
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.page = 'Login'
        st.experimental_rerun()  # Refresca la aplicación para aplicar cambios
