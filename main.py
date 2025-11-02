import sys
import tkinter as tk
from tkinter import messagebox
from src.database.db_config import DatabaseConfig
from src.gui.login_window import LoginWindow
from src.gui.admin_dashboard import AdminDashboard
from src.gui.faculty_dashboard import FacultyDashboard
from src.gui.student_dashboard import StudentDashboard

def main():
    print("Starting Student Academic Record Management System...")
    
    print("\n" + "="*60)
    print("  Student Academic Record Management System")
    print("="*60)
    print("\nInitializing database connection...")
    
    db_config = DatabaseConfig(
        host='localhost',
        user='root',
        password='',
        database='student_management'
    )
    
    print("Checking database connection...")
    if not db_config.connect():
        print("\nERROR: Could not connect to MySQL database!")
        print("\nPlease ensure:")
        print("  1. MySQL server is running")
        print("  2. Database credentials are correct in src/database/db_config.py")
        print("  3. Database 'student_management' exists or will be created\n")
        
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno(
            "Database Connection Error",
            "Could not connect to MySQL database!\n\n"
            "Would you like to initialize the database?\n\n"
            "Make sure MySQL is running and credentials are correct."
        )
        root.destroy()
        
        if result:
            print("\nAttempting to initialize database...")
            if db_config.initialize_database():
                print("Database initialized successfully!")
                db_config.connect()
            else:
                print("Failed to initialize database. Please check MySQL connection.")
                sys.exit(1)
        else:
            sys.exit(1)
    
    print("Database connected successfully!\n")
    
    print("Default Login Credentials:")
    print("-" * 40)
    print("Admin:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nNote: You can add faculty and students through admin panel")
    print("-" * 40 + "\n")
    
    while True:
        print("Opening login window...")
        login_window = LoginWindow(db_config)
        user_data = login_window.run()
        
        if not user_data:
            print("\nLogin cancelled. Exiting application...")
            break
        
        print(f"\nLogin successful!")
        print(f"Role: {user_data['role']}")
        print(f"Username: {user_data['username']}")
        
        if user_data['role'] == 'admin':
            print("Opening Admin Dashboard...")
            dashboard = AdminDashboard(db_config, user_data)
            dashboard.run()
        elif user_data['role'] == 'faculty':
            print("Opening Faculty Dashboard...")
            dashboard = FacultyDashboard(db_config, user_data)
            dashboard.run()
        elif user_data['role'] == 'student':
            print("Opening Student Dashboard...")
            dashboard = StudentDashboard(db_config, user_data)
            dashboard.run()
        
        print("\nDashboard closed. Returning to login...")
    
    db_config.disconnect()
    print("\nThank you for using Student Academic Record Management System!")
    print("Application terminated.\n")

if __name__ == "__main__":
    main()
