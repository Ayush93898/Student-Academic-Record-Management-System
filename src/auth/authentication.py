import hashlib
from src.database.db_config import DatabaseConfig

class Authentication:
    def __init__(self, db_config):
        self.db = db_config
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, password, role):
        hashed_password = self.hash_password(password)
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        last_id = self.db.execute_query(query, (username, hashed_password, role))
        return last_id
    
    def verify_login(self, username, password):
        hashed_password = self.hash_password(password)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        user = self.db.fetch_one(query, (username, hashed_password))
        return user
    
    def get_user_details(self, user_id, role):
        if role == 'student':
            query = """SELECT s.*, u.username FROM students s 
                       JOIN users u ON s.user_id = u.user_id 
                       WHERE s.user_id = %s"""
        elif role == 'faculty':
            query = """SELECT f.*, u.username FROM faculty f 
                       JOIN users u ON f.user_id = u.user_id 
                       WHERE f.user_id = %s"""
        else:
            query = "SELECT * FROM users WHERE user_id = %s"
        
        return self.db.fetch_one(query, (user_id,))
    
    def change_password(self, user_id, old_password, new_password):
        old_hashed = self.hash_password(old_password)
        query = "SELECT * FROM users WHERE user_id = %s AND password = %s"
        user = self.db.fetch_one(query, (user_id, old_hashed))
        
        if user:
            new_hashed = self.hash_password(new_password)
            update_query = "UPDATE users SET password = %s WHERE user_id = %s"
            self.db.execute_query(update_query, (new_hashed, user_id))
            return True
        return False
