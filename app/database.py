import mysql.connector
from mysql.connector import Error
import hashlib
import pandas as pd

# ==========================================
# DATABASE CONNECTION
# ==========================================
def get_connection():
    """Establishes a connection to the local MySQL server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='hela_hr_db'
        )
        return connection
    except Error as e:
        print(f"🚨 Error connecting to MySQL: {e}")
        return None

# ==========================================
# AUTHENTICATION LOGIC
# ==========================================
def hash_password(password):
    """Securely hashes passwords using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(username, password):
    """Checks the database for matching username, hashed password, and active status. Returns status dict."""
    conn = get_connection()
    if conn is None:
        return {"status": "error", "message": "Database connection failed."}
        
    cursor = conn.cursor(dictionary=True)
    hashed_input = hash_password(password)
    
    # First, check if the username exists
    cursor.execute("SELECT id, username, role, acc_sts, password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not user:
        return {"status": "error", "message": "User not found. Please check your username."}
        
    if user['password_hash'] != hashed_input:
        return {"status": "error", "message": "Invalid password."}
        
    if user['acc_sts'] != 1:
        return {"status": "error", "message": "Account is inactive. Please contact the administrator."}
        
    return {"status": "success", "user_data": user}

def initialize_admin():
    """Defensive Programming: Ensures the default admin exists on Day-1."""
    conn = get_connection()
    if conn is None:
        return
        
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        # Insert default admin: Hela123!
        default_hash = hash_password("Hela123!")
        insert_query = "INSERT INTO users (username, password_hash, role, acc_sts) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, ('admin', default_hash, 'ADMIN', 1))
        conn.commit()
        print("✅ Default Admin account created securely.")
        
    cursor.close()
    conn.close()

# ==========================================
# BATCH METRICS LOGIC (For your Dashboard)
# ==========================================
def log_batch_prediction(total, high_risk, stable):
    """Saves the results of a Bulk Upload to the MySQL database."""
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor()
        query = """
            INSERT INTO batch_metrics (total_records, high_risk_count, stable_count) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (total, high_risk, stable))
        conn.commit()
        cursor.close()
        conn.close()

def get_historical_metrics():
    """Fetches historical batch data for the Streamlit dashboard."""
    conn = get_connection()
    if conn is not None:
        query = "SELECT * FROM batch_metrics ORDER BY upload_date DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return pd.DataFrame() 

# ==========================================
# USER MANAGEMENT LOGIC (RBAC)
# ==========================================
def get_all_users():
    """Fetches all users excluding passwords for the Admin Dashboard."""
    conn = get_connection()
    if conn is not None:
        query = "SELECT id, username, role, acc_sts FROM users"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return pd.DataFrame()

def add_user(username, password, role, acc_sts):
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        query = "INSERT INTO users (username, password_hash, role, acc_sts) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (username, hashed_password, role, acc_sts))
            conn.commit()
            success = True
        except Error as e:
            print(f"🚨 Error adding user: {e}")
            success = False
        finally:
            cursor.close()
            conn.close()
        return success
    return False

def update_user_status(user_id, role, acc_sts):
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor()
        query = "UPDATE users SET role = %s, acc_sts = %s WHERE id = %s"
        try:
            cursor.execute(query, (role, acc_sts, user_id))
            conn.commit()
            success = True
        except Error as e:
            print(f"🚨 Error updating user: {e}")
            success = False
        finally:
            cursor.close()
            conn.close()
        return success
    return False

def reset_user_password(user_id, new_password):
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor()
        hashed_password = hash_password(new_password)
        query = "UPDATE users SET password_hash = %s WHERE id = %s"
        try:
            cursor.execute(query, (hashed_password, user_id))
            conn.commit()
            success = True
        except Error as e:
            print(f"🚨 Error resetting password: {e}")
            success = False
        finally:
            cursor.close()
            conn.close()
        return success
    return False

# Run this once when the script loads to ensure the DB is ready
initialize_admin()