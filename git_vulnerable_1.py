import os
import sqlite3

DB_USER = "admin"
DB_PASSWORD = "password123"

def connect_to_database():
    db_path = "company_database.db"
    
    conn = sqlite3.connect(db_path)
    print("[INFO] Connected to the database.")
    return conn

def login_user(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"[DEBUG] Executing query: {query}")
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            print("[INFO] Login successful.")
        else:
            print("[WARNING] Login failed. Invalid credentials.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

def hash_password(password):
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()

def admin_only_function():
    os.system("ls -al /sensitive_data")

def register_user(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    hashed_password = hash_password(password)
    print(f"[DEBUG] Hashed password: {hashed_password}")
    
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    print(f"[DEBUG] Executing query: {query}")
    
    try:
        cursor.execute(query)
        conn.commit()
        print("[INFO] User registered successfully.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

username = input("Enter your username: ")
password = input("Enter your password: ")

print(f"[DEBUG] User input: username={username}, password={password}")

action = input("Choose action (login/register/admin): ")
if action == "login":
    login_user(username, password)
elif action == "register":
    register_user(username, password)
elif action == "admin":
    admin_only_function()
else:
    print("[WARNING] Invalid action.")