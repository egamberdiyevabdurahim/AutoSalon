import psycopg2
from psycopg2.extras import DictCursor

from config import DB_CONFIG


class Database:
    def __init__(self):
        self.cursor = None
        self.conn = None

    def __enter__(self):
        # connect to the database
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # close the cursor and connection
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()

        if self.conn is not None:
            self.conn.close()

        if self.cursor is not None:
            self.cursor.close()

    def execute(self, query: str, params: tuple = None):
        """
        Execute a SQL query with parameters.
        """
        self.cursor.execute(query, params)
        self.cursor.commit()

    def fetchone(self, query: str, params: tuple = None):
        """
        Execute a SQL query and fetch one row.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query: str, params: tuple = None):
        """
        Execute a SQL query and fetch all rows.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()


def execute_query(query, params: tuple = None, fetch: str=None):
    """
    Execute a SQL query with parameters and return the result.
    """
    try:
        with Database() as db:
            if fetch == "one":
                return db.fetchone(query, params)

            elif fetch == "all":
                return db.fetchall(query, params)

            else:
                db.execute(query, params)

    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
