import streamlit as st
from modules.authentication.login import login_user
from modules.authentication.manage_users import manage_users
from modules.consultation.consultation import consultation_page
from modules.hospitalization.hospitalization import hospitalization_page
from modules.operation_rooms.operation_rooms import operating_rooms_page
from modules.emergency.emergency import emergency_page
from modules.ICU.icu import icu_page
from modules.authentication.logout import logout_user  # Asegúrate de tener logout.py

def main():
    # Verifica el estado de sesión para determinar la página a mostrar
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.session_state.page = 'Login'
    elif 'page' not in st.session_state or st.session_state.page not in ["Manage Users", "Consultations", "Hospitalization", "Operating Rooms", "Emergency", "ICU"]:
        st.session_state.page = 'Consultations'  # Página por defecto después del login

    col1, col2 = st.columns([1,4])
    with col1:
        st.image('AImedicare_logo.png', width=100)
    with col2:        
        st.subheader(":blue[AI Medicare], your hospital management system")
    # Muestra la página de inicio de sesión si no está autenticado
    if st.session_state.page == 'Login':
        login_user()
    else:
        # Muestra el menú lateral con opciones según el rol del usuario
        role = st.session_state.role
        st.sidebar.title("Hospital Management System")
        
        # Define el menú de opciones basado en el rol
        if role == "admin":
            modules = ["Manage Users", "Consultations", "Hospitalization", "Operating Rooms", "Emergency", "ICU"]
        elif role == "staff":
            modules = ["Consultations"]  # Agrega más módulos según los permisos del staff
        else:
            modules = []  # No debería llegar aquí, pero maneja un caso por defecto
        
        # Agregar la opción de Logout al menú
        choice = st.sidebar.selectbox("Select Module", modules + ["Logout"], index=modules.index(st.session_state.page) if st.session_state.page in modules else 0)
        
        # Mostrar la página correspondiente según la opción seleccionada
        if choice == "Logout":
            logout_user()
        elif choice == "Manage Users":
            manage_users()
        elif choice == "Consultations":
            consultation_page()
        elif choice == "Hospitalization":
            hospitalization_page()
        elif choice == "Operating Rooms":
            operating_rooms_page()
        elif choice == "Emergency":
            emergency_page()
        elif choice == "ICU":
            icu_page()

if __name__ == "__main__":
    main()
