import tkinter as tk
from tkinter import ttk, messagebox
from src.database.db_operations import DatabaseOperations
from src.utils.helpers import center_window, show_message, clear_frame

class StudentDashboard:
    def __init__(self, db_config, user_data):
        self.db_config = db_config
        self.db_ops = DatabaseOperations(db_config)
        self.user_data = user_data
        self.student_id = user_data['details']['student_id'] if user_data['details'] else None
        
        self.window = tk.Tk()
        self.window.title("Student Dashboard - Student Management System")
        self.window.geometry("1000x600")
        center_window(self.window, 1000, 600)
        
        self.setup_ui()
    
    def setup_ui(self):
        header = tk.Frame(self.window, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Student Dashboard", font=('Arial', 18, 'bold'), 
                bg='#2c3e50', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        name = self.user_data['details']['name'] if self.user_data['details'] else self.user_data['username']
        tk.Label(header, text=f"Welcome, {name}", 
                font=('Arial', 11), bg='#2c3e50', fg='white').pack(side=tk.RIGHT, padx=20)
        
        sidebar = tk.Frame(self.window, bg='#34495e', width=180)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        buttons = [
            ("My Profile", self.view_profile),
            ("My Attendance", self.view_attendance),
            ("My Marks", self.view_marks),
            ("Performance Report", self.view_report),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, command=command, bg='#2c3e50', 
                          fg='white', font=('Arial', 10), width=16, height=2, 
                          cursor='hand2', relief=tk.FLAT)
            btn.pack(pady=5, padx=10)
        
        self.content_frame = tk.Frame(self.window, bg='white')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.view_profile()
    
    def view_profile(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="My Profile", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        if not self.student_id:
            tk.Label(self.content_frame, text="No profile data available", 
                    font=('Arial', 12), bg='white', fg='red').pack(pady=50)
            return
        
        student = self.db_ops.get_student_by_id(self.student_id)
        
        if student:
            profile_frame = tk.Frame(self.content_frame, bg='#ecf0f1', relief=tk.RIDGE, bd=2)
            profile_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
            
            fields = [
                ('Roll Number', student['roll_number']),
                ('Name', student['name']),
                ('Email', student['email']),
                ('Phone', student['phone']),
                ('Date of Birth', student['date_of_birth']),
                ('Gender', student['gender']),
                ('Semester', student['semester']),
                ('Status', student['status']),
                ('Address', student['address'])
            ]
            
            for i, (label, value) in enumerate(fields):
                tk.Label(profile_frame, text=f"{label}:", font=('Arial', 11, 'bold'), 
                        bg='#ecf0f1').grid(row=i, column=0, sticky='w', pady=8, padx=20)
                tk.Label(profile_frame, text=str(value), font=('Arial', 11), 
                        bg='#ecf0f1').grid(row=i, column=1, sticky='w', pady=8, padx=20)
    
    def view_attendance(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="My Attendance", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        if not self.student_id:
            tk.Label(self.content_frame, text="No attendance data available", 
                    font=('Arial', 12), bg='white', fg='red').pack(pady=50)
            return
        
        frame = tk.Frame(self.content_frame, bg='white')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('Date', 'Subject', 'Status')
        tree = ttk.Treeview(frame, columns=columns, show='headings', 
                           yscrollcommand=scrollbar.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        scrollbar.config(command=tree.yview)
        
        attendance_records = self.db_ops.get_attendance(self.student_id)
        for record in attendance_records:
            tree.insert('', tk.END, values=(
                record['attendance_date'],
                record['subject_name'],
                record['status']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        subjects = self.db_ops.get_all_subjects()
        if subjects:
            summary_frame = tk.Frame(self.content_frame, bg='white')
            summary_frame.pack(pady=10)
            
            tk.Label(summary_frame, text="Attendance Percentage by Subject:", 
                    font=('Arial', 12, 'bold'), bg='white').pack()
            
            for subject in subjects:
                percentage = self.db_ops.get_attendance_percentage(self.student_id, subject['subject_id'])
                if percentage > 0:
                    color = '#27ae60' if percentage >= 75 else '#e74c3c'
                    tk.Label(summary_frame, 
                            text=f"{subject['subject_name']}: {percentage}%", 
                            font=('Arial', 10), bg='white', fg=color).pack()
    
    def view_marks(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="My Marks", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        if not self.student_id:
            tk.Label(self.content_frame, text="No marks data available", 
                    font=('Arial', 12), bg='white', fg='red').pack(pady=50)
            return
        
        frame = tk.Frame(self.content_frame, bg='white')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('Subject', 'Exam Type', 'Marks Obtained', 'Max Marks', 'Grade')
        tree = ttk.Treeview(frame, columns=columns, show='headings', 
                           yscrollcommand=scrollbar.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scrollbar.config(command=tree.yview)
        
        marks_records = self.db_ops.get_marks(self.student_id)
        for record in marks_records:
            tree.insert('', tk.END, values=(
                record['subject_name'],
                record['exam_type'],
                record['marks_obtained'],
                record['max_marks'],
                record['grade']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def view_report(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="Performance Report", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        if not self.student_id:
            tk.Label(self.content_frame, text="No report data available", 
                    font=('Arial', 12), bg='white', fg='red').pack(pady=50)
            return
        
        report_frame = tk.Frame(self.content_frame, bg='white')
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        student = self.db_ops.get_student_by_id(self.student_id)
        
        tk.Label(report_frame, text=f"Student: {student['name']}", 
                font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=5)
        tk.Label(report_frame, text=f"Roll Number: {student['roll_number']}", 
                font=('Arial', 11), bg='white').pack(anchor='w', pady=2)
        tk.Label(report_frame, text=f"Semester: {student['semester']}", 
                font=('Arial', 11), bg='white').pack(anchor='w', pady=2)
        
        tk.Label(report_frame, text="\nAttendance Summary:", 
                font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=10)
        
        subjects = self.db_ops.get_all_subjects()
        attendance_frame = tk.Frame(report_frame, bg='#ecf0f1', relief=tk.RIDGE, bd=1)
        attendance_frame.pack(fill=tk.X, pady=5)
        
        for subject in subjects:
            percentage = self.db_ops.get_attendance_percentage(self.student_id, subject['subject_id'])
            if percentage > 0:
                color = '#27ae60' if percentage >= 75 else '#e74c3c'
                label_frame = tk.Frame(attendance_frame, bg='#ecf0f1')
                label_frame.pack(fill=tk.X, padx=10, pady=3)
                tk.Label(label_frame, text=f"{subject['subject_name']}: ", 
                        font=('Arial', 10), bg='#ecf0f1').pack(side=tk.LEFT)
                tk.Label(label_frame, text=f"{percentage}%", 
                        font=('Arial', 10, 'bold'), bg='#ecf0f1', fg=color).pack(side=tk.LEFT)
        
        tk.Label(report_frame, text="\nAcademic Performance:", 
                font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=10)
        
        marks_records = self.db_ops.get_marks(self.student_id)
        
        if marks_records:
            subject_marks = {}
            for record in marks_records:
                subject = record['subject_name']
                if subject not in subject_marks:
                    subject_marks[subject] = []
                subject_marks[subject].append({
                    'exam': record['exam_type'],
                    'marks': record['marks_obtained'],
                    'max': record['max_marks'],
                    'grade': record['grade']
                })
            
            marks_frame = tk.Frame(report_frame, bg='#ecf0f1', relief=tk.RIDGE, bd=1)
            marks_frame.pack(fill=tk.X, pady=5)
            
            for subject, exams in subject_marks.items():
                tk.Label(marks_frame, text=f"\n{subject}:", 
                        font=('Arial', 10, 'bold'), bg='#ecf0f1').pack(anchor='w', padx=10)
                for exam in exams:
                    tk.Label(marks_frame, 
                            text=f"  {exam['exam']}: {exam['marks']}/{exam['max']} (Grade: {exam['grade']})", 
                            font=('Arial', 9), bg='#ecf0f1').pack(anchor='w', padx=20)
        else:
            tk.Label(report_frame, text="No marks recorded yet", 
                    font=('Arial', 10), bg='white', fg='gray').pack(anchor='w')
    
    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            self.window.destroy()
    
    def run(self):
        self.window.mainloop()
