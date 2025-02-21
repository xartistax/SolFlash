import psycopg2
from psycopg2 import sql
from contextlib import contextmanager

from services.logger import setup_logger

logger = setup_logger("POSGRESS TASKS")

class PostgresDB:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish a connection to the database."""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            logger.info("Connection established.")
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def close(self):
        """Close the connection to the database."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Connection closed.")

    def execute_query(self, query, params=None):
        """Execute a read-only query (e.g., SELECT)."""
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            logger.info(f"Query executed successfully: {query}")
            return result
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None

    def execute_update(self, query, params=None):
        """Execute a query that modifies the database (e.g., INSERT, UPDATE, DELETE)."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            logger.info(f"Query executed and changes committed: {query}")
        except Exception as e:
            logger.error(f"Error executing update: {e}")
            self.connection.rollback()

    @contextmanager
    def transaction(self):
        """Context manager to automatically commit/rollback transactions."""
        try:
            yield self
            self.connection.commit()
        except Exception as e:
            logger.error(f"Error in transaction: {e}")
            self.connection.rollback()
            raise

    def create_table(self, table_name, columns):
        """Create a table in the database."""
        columns_str = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});"
        self.execute_update(query)
        logger.info(f"Table created or verified: {table_name}")

    def insert_record(self, table_name, data):
        """Insert a record into a table."""
        columns = ", ".join(data.keys())
        values = ", ".join([f"%s" for _ in data])
        query = sql.SQL(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
        self.execute_update(query, tuple(data.values()))
        logger.info(f"Record inserted into {table_name}: {data}")

    def update_record(self, table_name, data, condition):
        """Update a record in the table."""
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        condition_clause = " AND ".join([f"{key} = %s" for key in condition.keys()])
        query = sql.SQL(f"UPDATE {table_name} SET {set_clause} WHERE {condition_clause}")
        self.execute_update(query, tuple(data.values()) + tuple(condition.values()))
        logger.info(f"Record updated in {table_name}: {data} WHERE {condition}")

    def delete_record(self, table_name, condition):
        """Delete a record from the table."""
        condition_clause = " AND ".join([f"{key} = %s" for key in condition.keys()])
        query = sql.SQL(f"DELETE FROM {table_name} WHERE {condition_clause}")
        self.execute_update(query, tuple(condition.values()))
        logger.info(f"Record deleted from {table_name} WHERE {condition}")

    def fetch_records(self, table_name, condition=None):
        """Fetch records from a table."""
        if condition:
            condition_clause = " AND ".join([f"{key} = %s" for key in condition.keys()])
            query = f"SELECT * FROM {table_name} WHERE {condition_clause}"
            result = self.execute_query(query, tuple(condition.values()))
            logger.info(f"Records fetched from {table_name} WHERE {condition}")
            return result
        else:
            query = f"SELECT * FROM {table_name}"
            result = self.execute_query(query)
            logger.info(f"Records fetched from {table_name}")
            return result


    def truncate_table(self, table_name):
        """Truncate a table in the database (remove all records)."""
        try:
            query = sql.SQL("TRUNCATE TABLE {}").format(sql.Identifier(table_name))
            self.execute_update(query)
            logger.info(f"Table truncated: {table_name}")
        except Exception as e:
            logger.error(f"Error truncating table {table_name}: {e}")
