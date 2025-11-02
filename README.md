# Student Academic Record Management System

A comprehensive database-driven application for managing student academic records, built with Python, MySQL, and Tkinter.

## Features

### Role-Based Access Control
- **Admin**: Full system access
  - Add/Update/Delete students
  - Manage courses and subjects
  - View all student records
  
- **Faculty**: Academic operations
  - Mark student attendance
  - Enter and view student marks
  - View attendance records
  
- **Student**: View-only access
  - View personal profile
  - Check attendance records
  - View marks and grades
  - Generate performance reports

### Core Functionality
- Student registration with complete profile management
- Course and subject management
- Attendance tracking with date/time stamps
- Marks entry with automatic grade calculation
- Performance report generation with attendance percentage
- Secure login with SHA-256 password encryption

## Prerequisites

1. **Python 3.11+** (installed)
2. **MySQL Server** (must be running)
3. **Required Libraries**:
   - mysql-connector-python
   - Pillow
   - tkinter (built-in)

## Installation

The required Python packages are already installed:
```bash
pip install mysql-connector-python pillow
```

## Database Setup

### Option 1: Automatic Setup
The application will automatically create and initialize the database on first run if it doesn't exist.

### Option 2: Manual Setup
1. Start MySQL server
2. Update database credentials in `src/database/db_config.py` if needed
3. Run the initialization script:
```bash
mysql -u root -p < src/database/db_init.sql
```

### Default Database Configuration
- **Host**: localhost
- **User**: root
- **Password**: (empty)
- **Database**: student_management

Update these in `src/database/db_config.py` if your setup is different.

## Running the Application

```bash
python main.py
```

## Default Login Credentials

### Admin Account
- **Username**: admin
- **Password**: admin123

### Sample Faculty Account
- **Username**: faculty1
- **Password**: faculty123
- **Faculty**: Dr. John Smith (FAC001)

### Sample Student Account
- **Username**: student1
- **Password**: student123
- **Student**: Alice Johnson (CSE2024001)

### Creating Additional Accounts
Use the admin dashboard to:
1. Add new students (creates login automatically)
2. Add faculty members (requires separate user creation)

## Database Schema

The system uses the following tables:

- **users**: Authentication data for all users
- **students**: Student personal and enrollment information
- **faculty**: Faculty member details
- courses**: Course master data
- **subjects**: Subject details linked to courses
- **attendance**: Daily attendance records
- **marks**: Student marks and grades

## Grade Calculation

Automatic grading based on percentage:
- **A+**: 90% and above
- **A**: 80-89%
- **B+**: 70-79%
- **B**: 60-69%
- **C**: 50-59%
- **D**: 40-49%
- **F**: Below 40%

## Project Structure

```
/
├── main.py                     # Application entry point
├── src/
│   ├── database/
│   │   ├── db_config.py       # Database connection
│   │   ├── db_init.sql        # Schema initialization
│   │   └── db_operations.py   # CRUD operations
│   ├── auth/
│   │   └── authentication.py  # Login & authentication
│   ├── gui/
│   │   ├── login_window.py    # Login interface
│   │   ├── admin_dashboard.py # Admin interface
│   │   ├── faculty_dashboard.py # Faculty interface
│   │   └── student_dashboard.py # Student interface
│   └── utils/
│       └── helpers.py         # Utility functions
└── README.md
```

## Usage Guide

### Admin Operations
1. **Add Student**: Provide username, password, and student details
2. **Update Student**: Search by roll number, modify details
3. **Delete Student**: Mark student as inactive
4. **Add Course/Subject**: Manage academic structure

### Faculty Operations
1. **Mark Attendance**: Select subject, date, student, and status
2. **Enter Marks**: Select subject, exam type, and marks
3. **View Records**: Search by roll number

### Student Operations
1. **View Profile**: See personal details
2. **Check Attendance**: View attendance with percentage
3. **View Marks**: See marks and grades for all subjects
4. **Performance Report**: Comprehensive academic summary

## Troubleshooting

### Database Connection Failed
- Ensure MySQL server is running
- Check credentials in `src/database/db_config.py`
- Verify database 'student_management' exists

### Login Failed
- Check username and password
- Ensure correct role is selected
- Verify user exists in database

### GUI Not Showing
- Ensure tkinter is installed (comes with Python)
- Check for X11/display server if on Linux

## Security Notes

- Passwords are encrypted using SHA-256
- Never share database credentials
- Change default admin password after first login
- Regular database backups recommended

## Future Enhancements

- Data backup and recovery functionality
- PDF report generation
- Bulk data import
- Advanced search and filtering
- Academic calendar integration
- Email notifications

## Support

For issues or questions, please check:
1. Database connection and credentials
2. MySQL server status
3. Python and library versions

---

**Developed for educational institutions to digitize academic record management.**
