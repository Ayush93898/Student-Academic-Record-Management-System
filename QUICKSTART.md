# Quick Start Guide

## Getting Started in 5 Minutes

### Step 1: Install MySQL
Choose one option:
- **Windows**: Download [XAMPP](https://www.apachefriends.org/) → Start MySQL
- **Mac**: `brew install mysql && brew services start mysql`
- **Linux**: `sudo apt install mysql-server && sudo systemctl start mysql`

### Step 2: Run the Application
```bash
python main.py
```

The application will automatically:
- Connect to MySQL
- Create the database
- Initialize all tables
- Insert sample data

### Step 3: Login

#### As Administrator
- Username: `admin`
- Password: `admin123`
- **Can**: Add students, manage courses, view all records

#### As Faculty
- Username: `faculty1`
- Password: `faculty123`
- **Can**: Mark attendance, enter marks, view student records

#### As Student
- Username: `student1`
- Password: `student123`
- **Can**: View profile, attendance, marks, and performance report

## What You Can Do

### Admin Dashboard
1. **View Students** - See all enrolled students
2. **Add Student** - Register new student with login credentials
3. **Update Student** - Modify student information
4. **Delete Student** - Mark student as inactive
5. **Add Course** - Create new courses
6. **Add Subject** - Add subjects to courses

### Faculty Dashboard
1. **Mark Attendance** - Record daily attendance for students
2. **View Attendance** - Check student attendance records
3. **Enter Marks** - Input marks for exams (Internal 1/2/3, Semester, Final)
4. **View Marks** - See student performance

### Student Dashboard
1. **My Profile** - View personal information
2. **My Attendance** - See attendance records with percentage
3. **My Marks** - View marks and grades
4. **Performance Report** - Complete academic summary

## Sample Data Included

The database comes pre-loaded with:
- 3 Courses (CSE, ECE, ME)
- 4 Subjects (Programming, Data Structures, DBMS, Math)
- 1 Faculty (Dr. John Smith)
- 1 Student (Alice Johnson - CSE Semester 1)

## Common Tasks

### Add a New Student (Admin)
1. Login as admin
2. Click "Add Student"
3. Fill in username, password, roll number, and details
4. Select course and semester
5. Click "Add Student"

### Mark Attendance (Faculty)
1. Login as faculty
2. Click "Mark Attendance"
3. Select subject and date
4. Enter student roll number
5. Choose status (Present/Absent/Leave)
6. Click "Mark Attendance"

### View Performance Report (Student)
1. Login as student
2. Click "Performance Report"
3. See attendance percentage and marks for all subjects

## Troubleshooting

**Can't connect to MySQL?**
- Ensure MySQL is running
- Check credentials in `src/database/db_config.py`
- Default: host=localhost, user=root, password=(empty)

**Login failed?**
- Make sure database is initialized
- Check username and role match
- Verify password is correct

**Need help?**
See `SETUP_GUIDE.md` for detailed MySQL installation instructions.

---

**That's it! You're ready to manage student records efficiently.**
