import streamlit as st
import sqlite3
from hashlib import sha256

translations = {
    "es": {
        "title": "Gestionar Usuarios",
        "existing": "Usuarios Existentes",
        "add": "Agregar Nuevo Usuario",
        "new_username": "Nuevo Usuario",
        "new_password": "Nueva Contraseña",
        "role": "Rol",
        "create": "Crear Usuario",
        "created": "Usuario {username} creado exitosamente",
        "update": "Actualizar Usuario",
        "user_id_update": "ID de Usuario a Actualizar",
        "updated_username": "Usuario Actualizado",
        "updated_password": "Contraseña Actualizada",
        "updated_role": "Rol Actualizado",
        "update_btn": "Actualizar Usuario",
        "updated": "Usuario ID {user_id} actualizado exitosamente",
        "delete": "Eliminar Usuario",
        "user_id_delete": "ID de Usuario a Eliminar",
        "delete_btn": "Eliminar Usuario",
        "deleted": "Usuario ID {user_id} eliminado exitosamente"
    },
    "en": {
        "title": "Manage Users",
        "existing": "Existing Users",
        "add": "Add New User",
        "new_username": "New Username",
        "new_password": "New Password",
        "role": "Role",
        "create": "Create User",
        "created": "User {username} created successfully",
        "update": "Update User",
        "user_id_update": "User ID to Update",
        "updated_username": "Updated Username",
        "updated_password": "Updated Password",
        "updated_role": "Updated Role",
        "update_btn": "Update User",
        "updated": "User ID {user_id} updated successfully",
        "delete": "Delete User",
        "user_id_delete": "User ID to Delete",
        "delete_btn": "Delete User",
        "deleted": "User ID {user_id} deleted successfully"
    }
}

def t(key, **kwargs):
    lang = st.session_state.get("language", "en")
    txt = translations[lang].get(key, key)
    return txt.format(**kwargs)

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def create_user(username, password, role):
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
    conn.commit()
    conn.close()

def update_user(user_id, username, password, role):
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?", (username, hashed_password, role, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def manage_users():
    st.title(t("title"))
    st.subheader(t("existing"))
    users = get_users()
    for user in users:
        st.write(f"ID: {user[0]}, Username: {user[1]}, Role: {user[3]}")

    st.subheader(t("add"))
    new_username = st.text_input(t("new_username"))
    new_password = st.text_input(t("new_password"), type='password')
    new_role = st.selectbox(t("role"), ["admin", "doctor", "nurse", "staff"])
    if st.button(t("create")):
        create_user(new_username, new_password, new_role)
        st.success(t("created", username=new_username))

    st.subheader(t("update"))
    user_id_to_update = st.number_input(t("user_id_update"), min_value=1, step=1)
    updated_username = st.text_input(t("updated_username"))
    updated_password = st.text_input(t("updated_password"), type='password')
    updated_role = st.selectbox(t("updated_role"), ["admin", "doctor", "nurse", "staff"])
    if st.button(t("update_btn")):
        update_user(user_id_to_update, updated_username, updated_password, updated_role)
        st.success(t("updated", user_id=user_id_to_update))

    st.subheader(t("delete"))
    user_id_to_delete = st.number_input(t("user_id_delete"), min_value=1, step=1)
    if st.button(t("delete_btn")):
        delete_user(user_id_to_delete)
        st.success(t("deleted", user_id=user_id_to_delete))
