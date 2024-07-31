import streamlit as st
import sqlite3
from hashlib import sha256

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
    st.title("Manage Users")
    
    # Display existing users
    st.subheader("Existing Users")
    users = get_users()
    for user in users:
        st.write(f"ID: {user[0]}, Username: {user[1]}, Role: {user[3]}")

    st.subheader("Add New User")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type='password')
    new_role = st.selectbox("Role", ["admin", "doctor", "nurse", "staff"])
    if st.button("Create User"):
        create_user(new_username, new_password, new_role)
        st.success(f"User {new_username} created successfully")

    st.subheader("Update User")
    user_id_to_update = st.number_input("User ID to Update", min_value=1, step=1)
    updated_username = st.text_input("Updated Username")
    updated_password = st.text_input("Updated Password", type='password')
    updated_role = st.selectbox("Updated Role", ["admin", "doctor", "nurse", "staff"])
    if st.button("Update User"):
        update_user(user_id_to_update, updated_username, updated_password, updated_role)
        st.success(f"User ID {user_id_to_update} updated successfully")

    st.subheader("Delete User")
    user_id_to_delete = st.number_input("User ID to Delete", min_value=1, step=1)
    if st.button("Delete User"):
        delete_user(user_id_to_delete)
        st.success(f"User ID {user_id_to_delete} deleted successfully")
