import mysql.connector
from mysql.connector import Error

class DatabaseConfig:
    def __init__(self, host='localhost', user='root', password='', database='student_management'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        cursor = None
        last_id = None
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            last_id = cursor.lastrowid
            return last_id
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def fetch_all(self, query, params=None):
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def fetch_one(self, query, params=None):
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def initialize_database(self):
        try:
            init_connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = init_connection.cursor()
            
            with open('src/database/db_init.sql', 'r') as f:
                sql_script = f.read()
            
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            
            init_connection.commit()
            cursor.close()
            init_connection.close()
            print("Database initialized successfully!")
            return True
        except Error as e:
            print(f"Error initializing database: {e}")
            return False
