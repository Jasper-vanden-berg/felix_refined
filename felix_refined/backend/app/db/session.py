import psycopg2
import psycopg2.extras

def get_conn():
    return psycopg2.connect(
        dbname="felix",
        user="felix",
        password="hersenbank",
        host="localhost",
        cursor_factory=psycopg2.extras.RealDictCursor
    )