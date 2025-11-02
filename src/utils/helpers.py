from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def validate_email(email):
    if '@' in email and '.' in email:
        return True
    return False

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

def format_date(date_str):
    try:
        date_obj = datetime.strptime(str(date_str), '%Y-%m-%d')
        return date_obj.strftime('%d-%m-%Y')
    except:
        return str(date_str)

def get_current_date():
    return datetime.now().strftime('%Y-%m-%d')

def show_message(title, message, msg_type='info'):
    if msg_type == 'info':
        messagebox.showinfo(title, message)
    elif msg_type == 'error':
        messagebox.showerror(title, message)
    elif msg_type == 'warning':
        messagebox.showwarning(title, message)
    elif msg_type == 'success':
        messagebox.showinfo(title, message)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
