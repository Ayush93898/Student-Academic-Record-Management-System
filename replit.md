# Student Academic Record Management System

## Overview
A comprehensive database-driven application for managing student academic records including personal details, course enrollment, attendance, marks, and grades. Built with Python (Tkinter GUI) and MySQL database.

**Created:** November 2, 2025  
**Status:** Active Development  
**Tech Stack:** Python 3.11, MySQL, Tkinter, mysql-connector-python

## Recent Changes
- 2025-11-02: Initial project setup with Python 3.11 and required dependencies
- 2025-11-02: Installed mysql-connector-python and Pillow libraries

## Project Architecture

### Directory Structure
```
/
├── main.py                 # Main application entry point
├── src/
│   ├── database/
│   │   ├── db_config.py   # Database connection configuration
│   │   ├── db_init.sql    # Database schema initialization
│   │   └── db_operations.py # CRUD operations
│   ├── auth/
│   │   └── authentication.py # Login and password encryption
│   ├── gui/
│   │   ├── login_window.py    # Login interface
│   │   ├── admin_dashboard.py # Admin interface
│   │   ├── faculty_dashboard.py # Faculty interface
│   │   └── student_dashboard.py # Student interface
│   └── utils/
│       └── helpers.py     # Utility functions
└── README.md              # User documentation
```

### Database Schema
**Tables:**
- `users` - Login credentials for all users (admin, faculty, student)
- `students` - Student personal and enrollment information
- `courses` - Course master data
- `subjects` - Subject details linked to courses
- `faculty` - Faculty/teacher information
- `attendance` - Daily attendance records
- `marks` - Student marks for subjects

### Key Features
1. **Role-Based Access Control**
   - Admin: Full system access, student/faculty management
   - Faculty: Attendance and marks entry
   - Student: View-only access to personal records

2. **Core Functionality**
   - Student registration and profile management
   - Attendance tracking with date/time
   - Marks entry and automatic grade calculation
   - Performance report generation
   - Search, update, and delete operations

3. **Security**
   - SHA-256 password encryption
   - Role-based authentication
   - Secure database connections

## MySQL Database Configuration
**Required Setup:**
- MySQL Server running locally or remotely
- Database name: `student_management`
- Default connection: localhost:3306
- Update credentials in `src/database/db_config.py`

**Important**: Replit doesn't provide MySQL by default. See `SETUP_GUIDE.md` for:
- Local MySQL installation instructions
- Remote database setup
- Docker-based MySQL setup
- Troubleshooting tips

## User Preferences
None specified yet.

## Dependencies
- Python 3.11
- mysql-connector-python (9.5.0)
- Pillow (12.0.0)
- tkinter (built-in)
- hashlib (built-in)
- datetime (built-in)

## Running the Application
```bash
python main.py
```

**Default Login Credentials:**
- Admin: username=`admin`, password=`admin123`
- Sample Faculty: username=`faculty1`, password=`faculty123` (Dr. John Smith)
- Sample Student: username=`student1`, password=`student123` (Alice Johnson)

## Notes
- Ensure MySQL server is running before starting the application
- Database will be auto-created on first run
- Session secret is managed via environment variable SESSION_SECRET
