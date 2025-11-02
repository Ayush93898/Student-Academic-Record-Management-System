import tkinter as tk
from tkinter import ttk, messagebox
from src.database.db_operations import DatabaseOperations
from src.utils.helpers import center_window, show_message, clear_frame, get_current_date
from datetime import datetime

class FacultyDashboard:
    def __init__(self, db_config, user_data):
        self.db_config = db_config
        self.db_ops = DatabaseOperations(db_config)
        self.user_data = user_data
        self.faculty_id = user_data['details']['faculty_id'] if user_data['details'] else None
        
        self.window = tk.Tk()
        self.window.title("Faculty Dashboard - Student Management System")
        self.window.geometry("1200x700")
        center_window(self.window, 1200, 700)
        
        self.setup_ui()
    
    def setup_ui(self):
        header = tk.Frame(self.window, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Faculty Dashboard", font=('Arial', 18, 'bold'), 
                bg='#2c3e50', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        name = self.user_data['details']['name'] if self.user_data['details'] else self.user_data['username']
        tk.Label(header, text=f"Welcome, {name}", 
                font=('Arial', 11), bg='#2c3e50', fg='white').pack(side=tk.RIGHT, padx=20)
        
        sidebar = tk.Frame(self.window, bg='#34495e', width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        buttons = [
            ("Mark Attendance", self.mark_attendance),
            ("View Attendance", self.view_attendance),
            ("Enter Marks", self.enter_marks),
            ("View Marks", self.view_marks),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, command=command, bg='#2c3e50', 
                          fg='white', font=('Arial', 10), width=18, height=2, 
                          cursor='hand2', relief=tk.FLAT)
            btn.pack(pady=5, padx=10)
        
        self.content_frame = tk.Frame(self.window, bg='white')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_welcome()
    
    def show_welcome(self):
        clear_frame(self.content_frame)
        tk.Label(self.content_frame, text="Faculty Dashboard", 
                font=('Arial', 20, 'bold'), bg='white').pack(pady=50)
        tk.Label(self.content_frame, text="Select an option from the menu", 
                font=('Arial', 12), bg='white', fg='gray').pack()
    
    def mark_attendance(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="Mark Attendance", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        form_frame = tk.Frame(self.content_frame, bg='white')
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Subject:", font=('Arial', 10), 
                bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=10)
        subjects = self.db_ops.get_all_subjects()
        subject_dict = {f"{s['subject_code']} - {s['subject_name']}": s['subject_id'] for s in subjects}
        subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(form_frame, textvariable=subject_var, 
                                    values=list(subject_dict.keys()), 
                                    state='readonly', font=('Arial', 10), width=40)
        subject_combo.grid(row=0, column=1, pady=5, padx=10)
        if subject_dict:
            subject_combo.current(0)
        
        tk.Label(form_frame, text="Date:", font=('Arial', 10), 
                bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=10)
        date_entry = tk.Entry(form_frame, font=('Arial', 10), width=42)
        date_entry.insert(0, get_current_date())
        date_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Roll Number:", font=('Arial', 10), 
                bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=10)
        roll_entry = tk.Entry(form_frame, font=('Arial', 10), width=42)
        roll_entry.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Status:", font=('Arial', 10), 
                bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=10)
        status_var = tk.StringVar(value='Present')
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, 
                                   values=['Present', 'Absent', 'Leave'], 
                                   state='readonly', font=('Arial', 10), width=40)
        status_combo.grid(row=3, column=1, pady=5, padx=10)
        
        def submit():
            try:
                roll_number = roll_entry.get().strip()
                student = self.db_ops.get_student_by_roll(roll_number)
                
                if not student:
                    show_message("Error", "Student not found!", "error")
                    return
                
                subject_id = subject_dict[subject_var.get()]
                date = date_entry.get().strip()
                status = status_var.get()
                
                self.db_ops.mark_attendance(student['student_id'], subject_id, date, 
                                           status, self.faculty_id)
                show_message("Success", "Attendance marked successfully!", "success")
                roll_entry.delete(0, tk.END)
            except Exception as e:
                show_message("Error", f"Failed to mark attendance: {str(e)}", "error")
        
        tk.Button(form_frame, text="Mark Attendance", command=submit, bg='#27ae60', 
                 fg='white', font=('Arial', 11, 'bold'), width=20, 
                 cursor='hand2').grid(row=4, column=0, columnspan=2, pady=20)
    
    def view_attendance(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="View Attendance", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Roll Number:", font=('Arial', 10), 
                bg='white').pack(side=tk.LEFT, padx=5)
        roll_entry = tk.Entry(search_frame, font=('Arial', 10), width=20)
        roll_entry.pack(side=tk.LEFT, padx=5)
        
        result_frame = tk.Frame(self.content_frame, bg='white')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def search():
            clear_frame(result_frame)
            roll_number = roll_entry.get().strip()
            student = self.db_ops.get_student_by_roll(roll_number)
            
            if not student:
                show_message("Error", "Student not found!", "error")
                return
            
            tk.Label(result_frame, text=f"Attendance for {student['name']}", 
                    font=('Arial', 12, 'bold'), bg='white').pack(pady=10)
            
            scrollbar = tk.Scrollbar(result_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            columns = ('Date', 'Subject', 'Status')
            tree = ttk.Treeview(result_frame, columns=columns, show='headings', 
                               yscrollcommand=scrollbar.set)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=200)
            
            scrollbar.config(command=tree.yview)
            
            attendance_records = self.db_ops.get_attendance(student['student_id'])
            for record in attendance_records:
                tree.insert('', tk.END, values=(
                    record['attendance_date'],
                    record['subject_name'],
                    record['status']
                ))
            
            tree.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(search_frame, text="Search", command=search, bg='#3498db', 
                 fg='white', font=('Arial', 10, 'bold'), cursor='hand2').pack(side=tk.LEFT, padx=5)
    
    def enter_marks(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="Enter Marks", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        form_frame = tk.Frame(self.content_frame, bg='white')
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Roll Number:", font=('Arial', 10), 
                bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=10)
        roll_entry = tk.Entry(form_frame, font=('Arial', 10), width=40)
        roll_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Subject:", font=('Arial', 10), 
                bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=10)
        subjects = self.db_ops.get_all_subjects()
        subject_dict = {f"{s['subject_code']} - {s['subject_name']}": s['subject_id'] for s in subjects}
        subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(form_frame, textvariable=subject_var, 
                                    values=list(subject_dict.keys()), 
                                    state='readonly', font=('Arial', 10), width=38)
        subject_combo.grid(row=1, column=1, pady=5, padx=10)
        if subject_dict:
            subject_combo.current(0)
        
        tk.Label(form_frame, text="Exam Type:", font=('Arial', 10), 
                bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=10)
        exam_var = tk.StringVar(value='Internal 1')
        exam_combo = ttk.Combobox(form_frame, textvariable=exam_var, 
                                 values=['Internal 1', 'Internal 2', 'Internal 3', 'Semester', 'Final'], 
                                 state='readonly', font=('Arial', 10), width=38)
        exam_combo.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Marks Obtained:", font=('Arial', 10), 
                bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=10)
        marks_entry = tk.Entry(form_frame, font=('Arial', 10), width=40)
        marks_entry.grid(row=3, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Maximum Marks:", font=('Arial', 10), 
                bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=10)
        max_marks_entry = tk.Entry(form_frame, font=('Arial', 10), width=40)
        max_marks_entry.insert(0, '100')
        max_marks_entry.grid(row=4, column=1, pady=5, padx=10)
        
        def submit():
            try:
                roll_number = roll_entry.get().strip()
                student = self.db_ops.get_student_by_roll(roll_number)
                
                if not student:
                    show_message("Error", "Student not found!", "error")
                    return
                
                subject_id = subject_dict[subject_var.get()]
                exam_type = exam_var.get()
                marks_obtained = float(marks_entry.get().strip())
                max_marks = float(max_marks_entry.get().strip())
                
                if marks_obtained > max_marks:
                    show_message("Error", "Marks obtained cannot exceed maximum marks!", "error")
                    return
                
                self.db_ops.add_marks(student['student_id'], subject_id, exam_type, 
                                     marks_obtained, max_marks, self.faculty_id)
                show_message("Success", "Marks entered successfully!", "success")
                roll_entry.delete(0, tk.END)
                marks_entry.delete(0, tk.END)
            except ValueError:
                show_message("Error", "Please enter valid numeric marks!", "error")
            except Exception as e:
                show_message("Error", f"Failed to enter marks: {str(e)}", "error")
        
        tk.Button(form_frame, text="Submit Marks", command=submit, bg='#27ae60', 
                 fg='white', font=('Arial', 11, 'bold'), width=20, 
                 cursor='hand2').grid(row=5, column=0, columnspan=2, pady=20)
    
    def view_marks(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="View Marks", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Roll Number:", font=('Arial', 10), 
                bg='white').pack(side=tk.LEFT, padx=5)
        roll_entry = tk.Entry(search_frame, font=('Arial', 10), width=20)
        roll_entry.pack(side=tk.LEFT, padx=5)
        
        result_frame = tk.Frame(self.content_frame, bg='white')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def search():
            clear_frame(result_frame)
            roll_number = roll_entry.get().strip()
            student = self.db_ops.get_student_by_roll(roll_number)
            
            if not student:
                show_message("Error", "Student not found!", "error")
                return
            
            tk.Label(result_frame, text=f"Marks for {student['name']}", 
                    font=('Arial', 12, 'bold'), bg='white').pack(pady=10)
            
            scrollbar = tk.Scrollbar(result_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            columns = ('Subject', 'Exam Type', 'Marks', 'Max Marks', 'Grade')
            tree = ttk.Treeview(result_frame, columns=columns, show='headings', 
                               yscrollcommand=scrollbar.set)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            scrollbar.config(command=tree.yview)
            
            marks_records = self.db_ops.get_marks(student['student_id'])
            for record in marks_records:
                tree.insert('', tk.END, values=(
                    record['subject_name'],
                    record['exam_type'],
                    record['marks_obtained'],
                    record['max_marks'],
                    record['grade']
                ))
            
            tree.pack(fill=tk.BOTH, expand=True)
        
        tk.Button(search_frame, text="Search", command=search, bg='#3498db', 
                 fg='white', font=('Arial', 10, 'bold'), cursor='hand2').pack(side=tk.LEFT, padx=5)
    
    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            self.window.destroy()
    
    def run(self):
        self.window.mainloop()
