from app.config.database import get_connection
from pydantic import BaseModel, HttpUrl
from app.utils.base62 import generate_short_code

class URLCreate(BaseModel):
    original_url: HttpUrl

def create_url(original_url):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        while True:
            short_code = generate_short_code()
            query = """
                INSERT INTO urls (short_code, original_url)
                VALUES (%s, %s)
                RETURNING id, short_code, original_url, click_count;
            """
            try:
                cursor.execute(
                    query,
                    (short_code, str(original_url))
                )
                result = cursor.fetchone()
                connection.commit()
                return result
            except Exception as error:
                connection.rollback()
                if "unique_short_code" in str(error):
                    continue
                raise
    finally:
        cursor.close()
        connection.close()

def get_test_url():
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        select id, short_code, original_url, click_count
        from urls
        where short_code = %s;
    """

    cursor.execute(query, ("aB72x",))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    return result

def get_url_by_short_code(short_code):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
            SELECT id, short_code, original_url, click_count
            FROM urls
            WHERE short_code = %s;
        """
        cursor.execute(query, (short_code,))
        result = cursor.fetchone()
        return result
    finally:
        cursor.close()
        connection.close()

def increment_click_count(short_code):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
            UPDATE urls
            SET click_count = click_count + 1
            WHERE short_code = %s
        """
        cursor.execute(query, (short_code,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def delete_url(short_code):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
            DELETE FROM urls
            WHERE short_code = %s
        """
        cursor.execute(query, (short_code,))
        deleted_rows = cursor.rowcount
        connection.commit()
        return deleted_rows
    finally:
        cursor.close()
        connection.close()

def update_url(short_code, original_url):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
            UPDATE urls
            SET original_url = %s
            WHERE short_code = %s;
        """
        cursor.execute(
            query,(str(original_url), short_code))
        updated_rows = cursor.rowcount
        connection.commit()
        return updated_rows
    finally:
        cursor.close()
        connection.close()