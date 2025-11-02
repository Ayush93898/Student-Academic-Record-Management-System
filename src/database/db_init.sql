-- Active: 1762077113688@@127.0.0.1@3306@student_management


CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL,
    role ENUM('admin', 'faculty', 'student') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    duration INT NOT NULL,
    department VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subjects table
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    course_id INT,
    credits INT DEFAULT 3,
    semester INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

-- Faculty table
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    faculty_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    department VARCHAR(50),
    designation VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    address TEXT,
    course_id INT,
    semester INT DEFAULT 1,
    enrollment_date DATE,
    status ENUM('Active', 'Inactive', 'Graduated') DEFAULT 'Active',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
);

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status ENUM('Present', 'Absent', 'Leave') NOT NULL,
    marked_by INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (marked_by) REFERENCES faculty(faculty_id) ON DELETE SET NULL,
    UNIQUE KEY unique_attendance (student_id, subject_id, attendance_date)
);

-- Marks table
CREATE TABLE IF NOT EXISTS marks (
    mark_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    exam_type ENUM('Internal 1', 'Internal 2', 'Internal 3', 'Semester', 'Final') NOT NULL,
    marks_obtained DECIMAL(5,2),
    max_marks DECIMAL(5,2) DEFAULT 100,
    grade VARCHAR(2),
    entered_by INT,
    entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (entered_by) REFERENCES faculty(faculty_id) ON DELETE SET NULL
);

-- Insert default users
-- Admin user (password: admin123)
INSERT INTO users (username, password, role) VALUES 
('admin', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd4', 'admin')
ON DUPLICATE KEY UPDATE username=username;

-- Sample faculty user (password: faculty123)
INSERT INTO users (username, password, role) VALUES 
('faculty1', '9bbf0867f032c4a8d70c76f0e4ffb29eba6bf857d4b5de0e1d2a5c1c6c4c1e0f', 'faculty')
ON DUPLICATE KEY UPDATE username=username;

-- Sample student user (password: student123)
INSERT INTO users (username, password, role) VALUES 
('student1', '65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5', 'student')
ON DUPLICATE KEY UPDATE username=username;

-- Insert sample courses
INSERT INTO courses (course_code, course_name, duration, department) VALUES 
('CSE', 'Computer Science Engineering', 4, 'Engineering'),
('ECE', 'Electronics and Communication', 4, 'Engineering'),
('ME', 'Mechanical Engineering', 4, 'Engineering')
ON DUPLICATE KEY UPDATE course_code=course_code;

-- Insert sample subjects (dynamically linked to CSE course)
INSERT INTO subjects (subject_code, subject_name, course_id, credits, semester)
SELECT 'CS101', 'Programming in C', c.course_id, 4, 1
FROM courses c WHERE c.course_code = 'CSE'
ON DUPLICATE KEY UPDATE subject_code=subject_code;

INSERT INTO subjects (subject_code, subject_name, course_id, credits, semester)
SELECT 'CS102', 'Data Structures', c.course_id, 4, 2
FROM courses c WHERE c.course_code = 'CSE'
ON DUPLICATE KEY UPDATE subject_code=subject_code;

INSERT INTO subjects (subject_code, subject_name, course_id, credits, semester)
SELECT 'CS103', 'Database Management', c.course_id, 4, 3
FROM courses c WHERE c.course_code = 'CSE'
ON DUPLICATE KEY UPDATE subject_code=subject_code;

INSERT INTO subjects (subject_code, subject_name, course_id, credits, semester)
SELECT 'MATH101', 'Engineering Mathematics', c.course_id, 4, 1
FROM courses c WHERE c.course_code = 'CSE'
ON DUPLICATE KEY UPDATE subject_code=subject_code;

-- Insert sample faculty (dynamically linked to faculty1 user)
INSERT INTO faculty (user_id, faculty_code, name, email, phone, department, designation)
SELECT u.user_id, 'FAC001', 'Dr. John Smith', 'john.smith@university.edu', '9876543210', 'Computer Science', 'Professor'
FROM users u
WHERE u.username = 'faculty1'
ON DUPLICATE KEY UPDATE faculty_code=faculty_code;

-- Insert sample student (dynamically linked to student1 user and CSE course)
INSERT INTO students (user_id, roll_number, name, email, phone, date_of_birth, gender, address, course_id, semester, enrollment_date, status)
SELECT u.user_id, 'CSE2024001', 'Alice Johnson', 'alice.j@student.edu', '9123456789', '2005-03-15', 'Female', '123 Campus Road, City', c.course_id, 1, '2024-08-01', 'Active'
FROM users u
CROSS JOIN courses c
WHERE u.username = 'student1' AND c.course_code = 'CSE'
ON DUPLICATE KEY UPDATE roll_number=roll_number;
