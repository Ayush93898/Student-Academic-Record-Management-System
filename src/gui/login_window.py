import tkinter as tk
from tkinter import ttk, messagebox
from src.auth.authentication import Authentication
from src.utils.helpers import center_window

class LoginWindow:
    def __init__(self, db_config):
        self.db_config = db_config
        self.auth = Authentication(db_config)
        self.window = tk.Tk()
        self.window.title("Student Management System - Login")
        center_window(self.window, 400, 300)
        self.window.resizable(False, False)
        
        self.user_data = None
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = tk.Frame(self.window, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="Student Academic\nRecord Management System", 
                              font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
        login_frame = tk.Frame(main_frame, bg='#34495e', padx=30, pady=20)
        login_frame.pack()
        
        tk.Label(login_frame, text="Username:", font=('Arial', 11), bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = tk.Entry(login_frame, font=('Arial', 11), width=25)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(login_frame, text="Password:", font=('Arial', 11), bg='#34495e', fg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = tk.Entry(login_frame, font=('Arial', 11), width=25, show='*')
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(login_frame, text="Login As:", font=('Arial', 11), bg='#34495e', fg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.role_var = tk.StringVar(value='admin')
        role_combo = ttk.Combobox(login_frame, textvariable=self.role_var, 
                                  values=['admin', 'faculty', 'student'], 
                                  state='readonly', font=('Arial', 11), width=23)
        role_combo.grid(row=2, column=1, pady=5, padx=10)
        
        login_btn = tk.Button(login_frame, text="Login", command=self.login, 
                            bg='#27ae60', fg='white', font=('Arial', 11, 'bold'), 
                            width=20, cursor='hand2')
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        user = self.auth.verify_login(username, password)
        
        if user and user['role'] == role:
            user_details = self.auth.get_user_details(user['user_id'], role)
            self.user_data = {
                'user_id': user['user_id'],
                'username': user['username'],
                'role': user['role'],
                'details': user_details
            }
            self.window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username, password, or role!")
            self.password_entry.delete(0, tk.END)
    
    def run(self):
        self.window.mainloop()
        return self.user_data
