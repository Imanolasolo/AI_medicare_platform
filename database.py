import sqlite3

def create_connection():
    conn = sqlite3.connect('hospital.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Tabla de usuarios y roles
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL)''')

    # Agrega más tablas para consultas, hospitalización, etc.
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
