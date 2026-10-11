from pydantic import BaseModel
from app.config.database import get_connection
from app.utils.password import hash_password

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def create_user(username, email, password):
    password_hash = hash_password(password)
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id, username, email, created_at;
    """

    cursor.execute(
        query,
        (username, email, password_hash)
    )
    user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT id, username, email, password_hash
        FROM users
        WHERE email = %s;
    """
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT id, username, email
        FROM users
        WHERE id = %s;
    """
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user
