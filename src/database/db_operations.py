from src.database.db_config import DatabaseConfig

class DatabaseOperations:
    def __init__(self, db_config):
        self.db = db_config
    
    def add_student(self, user_id, roll_number, name, email, phone, dob, gender, address, course_id, semester):
        query = """INSERT INTO students (user_id, roll_number, name, email, phone, date_of_birth, 
                   gender, address, course_id, semester, enrollment_date) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"""
        params = (user_id, roll_number, name, email, phone, dob, gender, address, course_id, semester)
        return self.db.execute_query(query, params)
    
    def get_all_students(self):
        query = """SELECT s.*, c.course_name, u.username 
                   FROM students s 
                   LEFT JOIN courses c ON s.course_id = c.course_id 
                   LEFT JOIN users u ON s.user_id = u.user_id 
                   WHERE s.status = 'Active'"""
        return self.db.fetch_all(query)
    
    def get_student_by_id(self, student_id):
        query = "SELECT * FROM students WHERE student_id = %s"
        return self.db.fetch_one(query, (student_id,))
    
    def get_student_by_roll(self, roll_number):
        query = "SELECT * FROM students WHERE roll_number = %s"
        return self.db.fetch_one(query, (roll_number,))
    
    def update_student(self, student_id, name, email, phone, address, semester):
        query = """UPDATE students SET name=%s, email=%s, phone=%s, address=%s, semester=%s 
                   WHERE student_id=%s"""
        params = (name, email, phone, address, semester, student_id)
        return self.db.execute_query(query, params)
    
    def delete_student(self, student_id):
        query = "UPDATE students SET status='Inactive' WHERE student_id=%s"
        return self.db.execute_query(query, (student_id,))
    
    def add_faculty(self, user_id, faculty_code, name, email, phone, department, designation):
        query = """INSERT INTO faculty (user_id, faculty_code, name, email, phone, department, designation) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (user_id, faculty_code, name, email, phone, department, designation)
        return self.db.execute_query(query, params)
    
    def get_all_faculty(self):
        query = "SELECT * FROM faculty"
        return self.db.fetch_all(query)
    
    def get_all_courses(self):
        query = "SELECT * FROM courses"
        return self.db.fetch_all(query)
    
    def get_all_subjects(self, course_id=None):
        if course_id:
            query = "SELECT * FROM subjects WHERE course_id = %s"
            return self.db.fetch_all(query, (course_id,))
        else:
            query = "SELECT * FROM subjects"
            return self.db.fetch_all(query)
    
    def mark_attendance(self, student_id, subject_id, date, status, marked_by):
        query = """INSERT INTO attendance (student_id, subject_id, attendance_date, status, marked_by) 
                   VALUES (%s, %s, %s, %s, %s) 
                   ON DUPLICATE KEY UPDATE status=%s, marked_by=%s"""
        params = (student_id, subject_id, date, status, marked_by, status, marked_by)
        return self.db.execute_query(query, params)
    
    def get_attendance(self, student_id, subject_id=None):
        if subject_id:
            query = """SELECT a.*, s.subject_name FROM attendance a 
                       JOIN subjects s ON a.subject_id = s.subject_id 
                       WHERE a.student_id = %s AND a.subject_id = %s 
                       ORDER BY a.attendance_date DESC"""
            return self.db.fetch_all(query, (student_id, subject_id))
        else:
            query = """SELECT a.*, s.subject_name FROM attendance a 
                       JOIN subjects s ON a.subject_id = s.subject_id 
                       WHERE a.student_id = %s 
                       ORDER BY a.attendance_date DESC"""
            return self.db.fetch_all(query, (student_id,))
    
    def get_attendance_percentage(self, student_id, subject_id):
        query = """SELECT 
                   COUNT(*) as total,
                   SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present
                   FROM attendance 
                   WHERE student_id = %s AND subject_id = %s"""
        result = self.db.fetch_one(query, (student_id, subject_id))
        if result and result['total'] > 0:
            return round((result['present'] / result['total']) * 100, 2)
        return 0.0
    
    def add_marks(self, student_id, subject_id, exam_type, marks_obtained, max_marks, entered_by):
        grade = self.calculate_grade(marks_obtained, max_marks)
        query = """INSERT INTO marks (student_id, subject_id, exam_type, marks_obtained, max_marks, grade, entered_by) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (student_id, subject_id, exam_type, marks_obtained, max_marks, grade, entered_by)
        return self.db.execute_query(query, params)
    
    def get_marks(self, student_id, subject_id=None):
        if subject_id:
            query = """SELECT m.*, s.subject_name FROM marks m 
                       JOIN subjects s ON m.subject_id = s.subject_id 
                       WHERE m.student_id = %s AND m.subject_id = %s"""
            return self.db.fetch_all(query, (student_id, subject_id))
        else:
            query = """SELECT m.*, s.subject_name FROM marks m 
                       JOIN subjects s ON m.subject_id = s.subject_id 
                       WHERE m.student_id = %s"""
            return self.db.fetch_all(query, (student_id,))
    
    def calculate_grade(self, marks_obtained, max_marks):
        percentage = (marks_obtained / max_marks) * 100
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def add_course(self, course_code, course_name, duration, department):
        query = """INSERT INTO courses (course_code, course_name, duration, department) 
                   VALUES (%s, %s, %s, %s)"""
        params = (course_code, course_name, duration, department)
        return self.db.execute_query(query, params)
    
    def add_subject(self, subject_code, subject_name, course_id, credits, semester):
        query = """INSERT INTO subjects (subject_code, subject_name, course_id, credits, semester) 
                   VALUES (%s, %s, %s, %s, %s)"""
        params = (subject_code, subject_name, course_id, credits, semester)
        return self.db.execute_query(query, params)
