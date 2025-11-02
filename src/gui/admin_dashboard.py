import tkinter as tk
from tkinter import ttk, messagebox
from src.database.db_operations import DatabaseOperations
from src.auth.authentication import Authentication
from src.utils.helpers import center_window, show_message, clear_frame
from datetime import datetime

class AdminDashboard:
    def __init__(self, db_config, user_data):
        self.db_config = db_config
        self.db_ops = DatabaseOperations(db_config)
        self.auth = Authentication(db_config)
        self.user_data = user_data
        
        self.window = tk.Tk()
        self.window.title("Admin Dashboard - Student Management System")
        self.window.geometry("1200x700")
        center_window(self.window, 1200, 700)
        
        self.setup_ui()
    
    def setup_ui(self):
        header = tk.Frame(self.window, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Admin Dashboard", font=('Arial', 18, 'bold'), 
                bg='#2c3e50', fg='white').pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(header, text=f"Welcome, {self.user_data['username']}", 
                font=('Arial', 11), bg='#2c3e50', fg='white').pack(side=tk.RIGHT, padx=20)
        
        sidebar = tk.Frame(self.window, bg='#34495e', width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        buttons = [
            ("View Students", self.view_students),
            ("Add Student", self.add_student),
            ("Update Student", self.update_student),
            ("Delete Student", self.delete_student),
            ("Add Course", self.add_course),
            ("Add Subject", self.add_subject),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, command=command, bg='#2c3e50', 
                          fg='white', font=('Arial', 10), width=18, height=2, 
                          cursor='hand2', relief=tk.FLAT)
            btn.pack(pady=5, padx=10)
        
        self.content_frame = tk.Frame(self.window, bg='white')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.view_students()
    
    def view_students(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="All Students", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        frame = tk.Frame(self.content_frame, bg='white')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar_y = tk.Scrollbar(frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        columns = ('ID', 'Roll No', 'Name', 'Email', 'Phone', 'Course', 'Semester', 'Status')
        tree = ttk.Treeview(frame, columns=columns, show='headings', 
                           yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar_y.config(command=tree.yview)
        scrollbar_x.config(command=tree.xview)
        
        students = self.db_ops.get_all_students()
        for student in students:
            tree.insert('', tk.END, values=(
                student['student_id'],
                student['roll_number'],
                student['name'],
                student['email'],
                student['phone'],
                student.get('course_name', 'N/A'),
                student['semester'],
                student['status']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def add_student(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="Add New Student", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        form_frame = tk.Frame(self.content_frame, bg='white')
        form_frame.pack(pady=20)
        
        fields = {}
        labels = ['Username', 'Password', 'Roll Number', 'Name', 'Email', 'Phone', 
                 'Date of Birth (YYYY-MM-DD)', 'Address']
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", font=('Arial', 10), 
                    bg='white').grid(row=i, column=0, sticky='w', pady=5, padx=10)
            entry = tk.Entry(form_frame, font=('Arial', 10), width=30)
            if label == 'Password':
                entry.config(show='*')
            entry.grid(row=i, column=1, pady=5, padx=10)
            fields[label] = entry
        
        tk.Label(form_frame, text="Gender:", font=('Arial', 10), 
                bg='white').grid(row=len(labels), column=0, sticky='w', pady=5, padx=10)
        gender_var = tk.StringVar(value='Male')
        gender_combo = ttk.Combobox(form_frame, textvariable=gender_var, 
                                   values=['Male', 'Female', 'Other'], 
                                   state='readonly', font=('Arial', 10), width=28)
        gender_combo.grid(row=len(labels), column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Course:", font=('Arial', 10), 
                bg='white').grid(row=len(labels)+1, column=0, sticky='w', pady=5, padx=10)
        courses = self.db_ops.get_all_courses()
        course_dict = {f"{c['course_name']}": c['course_id'] for c in courses}
        course_var = tk.StringVar()
        course_combo = ttk.Combobox(form_frame, textvariable=course_var, 
                                   values=list(course_dict.keys()), 
                                   state='readonly', font=('Arial', 10), width=28)
        course_combo.grid(row=len(labels)+1, column=1, pady=5, padx=10)
        if course_dict:
            course_combo.current(0)
        
        tk.Label(form_frame, text="Semester:", font=('Arial', 10), 
                bg='white').grid(row=len(labels)+2, column=0, sticky='w', pady=5, padx=10)
        semester_var = tk.StringVar(value='1')
        semester_combo = ttk.Combobox(form_frame, textvariable=semester_var, 
                                     values=['1', '2', '3', '4', '5', '6', '7', '8'], 
                                     state='readonly', font=('Arial', 10), width=28)
        semester_combo.grid(row=len(labels)+2, column=1, pady=5, padx=10)
        
        def submit():
            try:
                username = fields['Username'].get().strip()
                password = fields['Password'].get().strip()
                
                if not username or not password:
                    show_message("Error", "Username and password are required!", "error")
                    return
                
                user_id = self.auth.create_user(username, password, 'student')
                if not user_id:
                    show_message("Error", "Username already exists!", "error")
                    return
                
                roll_number = fields['Roll Number'].get().strip()
                name = fields['Name'].get().strip()
                email = fields['Email'].get().strip()
                phone = fields['Phone'].get().strip()
                dob = fields['Date of Birth (YYYY-MM-DD)'].get().strip()
                address = fields['Address'].get().strip()
                gender = gender_var.get()
                course_id = course_dict[course_var.get()]
                semester = int(semester_var.get())
                
                self.db_ops.add_student(user_id, roll_number, name, email, phone, 
                                       dob, gender, address, course_id, semester)
                show_message("Success", "Student added successfully!", "success")
                self.view_students()
            except Exception as e:
                show_message("Error", f"Failed to add student: {str(e)}", "error")
        
        tk.Button(form_frame, text="Add Student", command=submit, bg='#27ae60', 
                 fg='white', font=('Arial', 11, 'bold'), width=20, cursor='hand2').grid(
                 row=len(labels)+3, column=0, columnspan=2, pady=20)
    
    def update_student(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="Update Student", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Roll Number:", font=('Arial', 10), 
                bg='white').pack(side=tk.LEFT, padx=5)
        roll_entry = tk.Entry(search_frame, font=('Arial', 10), width=20)
        roll_entry.pack(side=tk.LEFT, padx=5)
        
        form_frame = tk.Frame(self.content_frame, bg='white')
        form_frame.pack(pady=20)
        
        fields = {}
        
        def search_student():
            clear_frame(form_frame)
            roll_number = roll_entry.get().strip()
            student = self.db_ops.get_student_by_roll(roll_number)
            
            if not student:
                show_message("Error", "Student not found!", "error")
                return
            
            labels = ['Name', 'Email', 'Phone', 'Address', 'Semester']
            values = [student['name'], student['email'], student['phone'], 
                     student['address'], str(student['semester'])]
            
            for i, (label, value) in enumerate(zip(labels, values)):
                tk.Label(form_frame, text=label + ":", font=('Arial', 10), 
                        bg='white').grid(row=i, column=0, sticky='w', pady=5, padx=10)
                entry = tk.Entry(form_frame, font=('Arial', 10), width=30)
                entry.insert(0, value)
                entry.grid(row=i, column=1, pady=5, padx=10)
                fields[label] = entry
            
            def update():
                try:
                    name = fields['Name'].get().strip()
                    email = fields['Email'].get().strip()
                    phone = fields['Phone'].get().strip()
                    address = fields['Address'].get().strip()
                    semester = int(fields['Semester'].get().strip())
                    
                    self.db_ops.update_student(student['student_id'], name, email, 
                                              phone, address, semester)
                    show_message("Success", "Student updated successfully!", "success")
                    self.view_students()
                except Exception as e:
                    show_message("Error", f"Failed to update: {str(e)}", "error")
            
            tk.Button(form_frame, text="Update", command=update, bg='#3498db', 
                     fg='white', font=('Arial', 11, 'bold'), width=20, 
                     cursor='hand2').grid(row=len(labels), column=0, columnspan=2, pady=20)
        
        tk.Button(search_frame, text="Search", command=search_student, bg='#3498db', 
                 fg='white', font=('Arial', 10, 'bold'), cursor='hand2').pack(side=tk.LEFT, padx=5)
    
    def delete_student(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="Delete Student", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        frame = tk.Frame(self.content_frame, bg='white')
        frame.pack(pady=20)
        
        tk.Label(frame, text="Roll Number:", font=('Arial', 10), 
                bg='white').grid(row=0, column=0, pady=5, padx=10)
        roll_entry = tk.Entry(frame, font=('Arial', 10), width=30)
        roll_entry.grid(row=0, column=1, pady=5, padx=10)
        
        def delete():
            roll_number = roll_entry.get().strip()
            student = self.db_ops.get_student_by_roll(roll_number)
            
            if not student:
                show_message("Error", "Student not found!", "error")
                return
            
            if messagebox.askyesno("Confirm", f"Delete student {student['name']}?"):
                self.db_ops.delete_student(student['student_id'])
                show_message("Success", "Student deleted successfully!", "success")
                self.view_students()
        
        tk.Button(frame, text="Delete", command=delete, bg='#e74c3c', 
                 fg='white', font=('Arial', 11, 'bold'), width=20, 
                 cursor='hand2').grid(row=1, column=0, columnspan=2, pady=20)
    
    def add_course(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="Add New Course", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        frame = tk.Frame(self.content_frame, bg='white')
        frame.pack(pady=20)
        
        fields = {}
        labels = ['Course Code', 'Course Name', 'Duration (Years)', 'Department']
        
        for i, label in enumerate(labels):
            tk.Label(frame, text=label + ":", font=('Arial', 10), 
                    bg='white').grid(row=i, column=0, sticky='w', pady=5, padx=10)
            entry = tk.Entry(frame, font=('Arial', 10), width=30)
            entry.grid(row=i, column=1, pady=5, padx=10)
            fields[label] = entry
        
        def submit():
            try:
                code = fields['Course Code'].get().strip()
                name = fields['Course Name'].get().strip()
                duration = int(fields['Duration (Years)'].get().strip())
                department = fields['Department'].get().strip()
                
                self.db_ops.add_course(code, name, duration, department)
                show_message("Success", "Course added successfully!", "success")
                for field in fields.values():
                    field.delete(0, tk.END)
            except Exception as e:
                show_message("Error", f"Failed to add course: {str(e)}", "error")
        
        tk.Button(frame, text="Add Course", command=submit, bg='#27ae60', 
                 fg='white', font=('Arial', 11, 'bold'), width=20, 
                 cursor='hand2').grid(row=len(labels), column=0, columnspan=2, pady=20)
    
    def add_subject(self):
        clear_frame(self.content_frame)
        
        tk.Label(self.content_frame, text="Add New Subject", font=('Arial', 16, 'bold'), 
                bg='white').pack(pady=10)
        
        frame = tk.Frame(self.content_frame, bg='white')
        frame.pack(pady=20)
        
        tk.Label(frame, text="Subject Code:", font=('Arial', 10), 
                bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=10)
        code_entry = tk.Entry(frame, font=('Arial', 10), width=30)
        code_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Subject Name:", font=('Arial', 10), 
                bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=10)
        name_entry = tk.Entry(frame, font=('Arial', 10), width=30)
        name_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Course:", font=('Arial', 10), 
                bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=10)
        courses = self.db_ops.get_all_courses()
        course_dict = {f"{c['course_name']}": c['course_id'] for c in courses}
        course_var = tk.StringVar()
        course_combo = ttk.Combobox(frame, textvariable=course_var, 
                                   values=list(course_dict.keys()), 
                                   state='readonly', font=('Arial', 10), width=28)
        course_combo.grid(row=2, column=1, pady=5, padx=10)
        if course_dict:
            course_combo.current(0)
        
        tk.Label(frame, text="Credits:", font=('Arial', 10), 
                bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=10)
        credits_var = tk.StringVar(value='3')
        credits_combo = ttk.Combobox(frame, textvariable=credits_var, 
                                    values=['1', '2', '3', '4', '5'], 
                                    state='readonly', font=('Arial', 10), width=28)
        credits_combo.grid(row=3, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Semester:", font=('Arial', 10), 
                bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=10)
        semester_var = tk.StringVar(value='1')
        semester_combo = ttk.Combobox(frame, textvariable=semester_var, 
                                     values=['1', '2', '3', '4', '5', '6', '7', '8'], 
                                     state='readonly', font=('Arial', 10), width=28)
        semester_combo.grid(row=4, column=1, pady=5, padx=10)
        
        def submit():
            try:
                code = code_entry.get().strip()
                name = name_entry.get().strip()
                course_id = course_dict[course_var.get()]
                credits = int(credits_var.get())
                semester = int(semester_var.get())
                
                self.db_ops.add_subject(code, name, course_id, credits, semester)
                show_message("Success", "Subject added successfully!", "success")
                code_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
            except Exception as e:
                show_message("Error", f"Failed to add subject: {str(e)}", "error")
        
        tk.Button(frame, text="Add Subject", command=submit, bg='#27ae60', 
                 fg='white', font=('Arial', 11, 'bold'), width=20, 
                 cursor='hand2').grid(row=5, column=0, columnspan=2, pady=20)
    
    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            self.window.destroy()
    
    def run(self):
        self.window.mainloop()
