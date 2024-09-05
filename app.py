import streamlit as st
from modules.authentication.login import login_user
from modules.authentication.manage_users import manage_users
from modules.consultation.consultation import consultation_page
from modules.hospitalization.hospitalization import hospitalization_page
from modules.operation_rooms.operation_rooms import operating_rooms_page
from modules.emergency.emergency import emergency_page
from modules.ICU.icu import icu_page
from modules.authentication.logout import logout_user  # Asegúrate de tener logout.py
import base64

def main():

    # Configuración de la página
    st.set_page_config(page_title="AI Medicare Platform", page_icon="hospital", layout="wide")

    # Imagen de background de la pagina
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    img_base64 = get_base64_of_bin_file('background.jpg')

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url('data:image/jpeg;base64,{img_base64}') no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


    # Verifica el estado de sesión para determinar la página a mostrar
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.session_state.page = 'Login'
    elif 'page' not in st.session_state or st.session_state.page not in ["Manage Users", "Consultations", "Hospitalization", "Operating Rooms", "Emergency", "ICU"]:
        st.session_state.page = 'Consultations'  # Página por defecto después del login

    col1, col2, col3 = st.columns([1,4,2])
    with col1:
        st.image('AImedicare_logo.png', width=150)
    with col2:        
        st.subheader(":blue[AI Medicare], your hospital management system")
        st.write("Manage your health institution with our fully customizable AI based platform")
    with col3:
        with st.expander("Instructions to use the AI Medicare app"):
            st.markdown('''
                        1. Insert admin in Username area with :red[Ilargietaeguzki1.] password.
                        2. When in login page, use the options in the selector to manage users at your very own
                        3. To logout and change users use the selector area in the sidebar and check in :blue[logout], after it push the :red[logout] button in the dashboard area.
                        ''')


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
        elif role == "doctor":
            modules = ["Consultations","Hospitalization", "Operating Rooms"]  # Agrega más módulos según los permisos del staff
        elif role == "nurse":
            modules = ["ICU", "Operating Rooms"]    
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
