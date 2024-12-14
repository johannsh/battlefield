import os
import sqlite3

# 1. Захардкоженные учетные данные (Проблема: S105)
DB_USER = "admin"  # Никогда не храните учетные данные в коде
DB_PASSWORD = "password123"

# 2. Небезопасная передача пароля
def connect_to_database():
    # 3. Захардкоженный путь к базе данных (Проблема: S2083)
    db_path = "company_database.db"
    
    # 4. Никакого шифрования соединения
    conn = sqlite3.connect(db_path)
    print("[INFO] Connected to the database.")
    return conn

# 5. Небезопасная обработка пользовательского ввода
def login_user(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # 6. Прямое включение пользовательских данных в SQL-запрос (SQL Injection: S3649)
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

# 7. Использование устаревших и небезопасных хэшей для хранения паролей (MD5: S5334)
def hash_password(password):
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()

# 8. Уязвимость из-за неконтролируемого доступа к функциям
def admin_only_function():
    # 9. Потенциальный Command Injection через os.system (S2091)
    os.system("ls -al /sensitive_data")

# 10. Никакой проверки надежности пароля
def register_user(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # 11. Пароли хранятся в открытом виде
    hashed_password = hash_password(password)
    print(f"[DEBUG] Hashed password: {hashed_password}")
    
    # 12. SQL Injection во время регистрации
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

# 13. Никакой проверки ввода пользователя
username = input("Enter your username: ")
password = input("Enter your password: ")

# 14. Хранение введенного пароля в логах (Проблема: S5144)
print(f"[DEBUG] User input: username={username}, password={password}")

# 15. Выбор действия без проверки уровня доступа
action = input("Choose action (login/register/admin): ")
if action == "login":
    login_user(username, password)
elif action == "register":
    register_user(username, password)
elif action == "admin":
    admin_only_function()
else:
    print("[WARNING] Invalid action.")
