import psycopg

def get_connection():
    connection = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="url_shortener",
        user="postgres",
        password="Vikas@1011"
    )
    return connection