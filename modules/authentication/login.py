import streamlit as st
import sqlite3
from hashlib import sha256

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = sqlite3.connect(db_file)
    return conn

def login_user():
    st.title("Login")

    # Mostrar campos de entrada para usuario y contraseña
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    # Añadir un botón de login
    if st.button("Login"):
        # Hashear la contraseña
        hashed_password = sha256(password.encode()).hexdigest()
        
        # Crear conexión a la base de datos
        conn = create_connection('hospital.db')
        cursor = conn.cursor()
        
        # Ejecutar la consulta de autenticación
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()
        conn.close()
        
        # Validar el usuario
        if user:
            st.session_state.logged_in = True
            st.session_state.role = user[3]  # Suponiendo que el rol está en la 4ª columna
            st.session_state.username = user[1]
            
            # Establecer la página según el rol del usuario
            if user[3] == "admin":
                st.session_state.page = "Manage Users"  # Admin puede acceder a todas las páginas
            elif user[3] == "staff":
                st.session_state.page = "Consultations"  # Cambia según los permisos del staff
            else:
                st.error("Unknown role")
            
            # Redirigir a la página correspondiente
            st.experimental_rerun()
        else:
            st.error("Invalid Username or Password")
