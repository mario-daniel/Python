import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect('rfid')
cursor = conn.cursor()

def login():
    if student_button:
        cursor.execute('SELECT password FROM Student WHERE student_id = ?', (student_id.get(),))
        password_db = cursor.fetchall()
        cursor.execute('SELECT student_id FROM Student WHERE student_id = ?', (student_id.get(),))
        student_id_db = cursor.fetchall()
        if student_id_db == [] or password_db == []:
            messagebox.showerror("Login Failed", "User does not exist")
        elif student_password.get() == password_db[0][0]:
            cursor.execute('SELECT first_name, last_name FROM Student WHERE student_id = ?', (student_id.get(),))
            name = cursor.fetchall()
            messagebox.showinfo('Login Successful', f'Welcome, {name[0][0]} {name[0][1]}')
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")
    elif teacher_button:
        cursor.execute('SELECT password FROM Teacher WHERE teacher_id = ?', (teacher_id.get(),))
        password_db = cursor.fetchall()
        cursor.execute('SELECT teacher_id FROM Teacher WHERE teacher_id = ?', (teacher_id.get(),))
        teacher_id_db = cursor.fetchall()
        if teacher_id_db == [] or password_db == []:
            messagebox.showerror("Login Failed", "User does not exist")
        elif teacher_password.get() == password_db[0][0]:
            cursor.execute('SELECT first_name, last_name FROM Teacher WHERE teacher_id = ?', (teacher_id.get(),))
            name = cursor.fetchall()
            messagebox.showinfo('Login Successful', f'Welcome, {name[0][0]} {name[0][1]}')
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

window = tk.Tk()
window.geometry('400x200')
window.title('Student RFID')

#Vairables
student_id = tk.StringVar()
student_password = tk.StringVar()

teacher_id = tk.StringVar()
teacher_password = tk.StringVar()

#Frames
main_frame = ttk.Frame(window, width = 400, height = 200)
main_frame.pack()

frame_student = ttk.Frame(main_frame, borderwidth = 10, relief = tk.GROOVE)

frame_teacher = ttk.Frame(main_frame, borderwidth = 10, relief = tk.GROOVE)

#Widgets
student_id_label = ttk.Label(frame_student, text = 'Student ID')
student_id_label.pack()
student_id_entry = ttk.Entry(frame_student, textvariable = student_id)
student_id_entry.pack()
student_password_label = ttk.Label(frame_student, text = 'Password')
student_password_label.pack()
student_password_entry = ttk.Entry(frame_student, textvariable = student_password, show="*")
student_password_entry.pack()
student_button = ttk.Button(frame_student, text = 'Login', command = login)
student_button.pack()

teacher_id_label = ttk.Label(frame_teacher, text = 'teacher ID')
teacher_id_label.pack()
teacher_id_entry = ttk.Entry(frame_teacher, textvariable = teacher_id)
teacher_id_entry.pack()
teacher_password_label = ttk.Label(frame_teacher, text = 'Password')
teacher_password_label.pack()
teacher_password_entry = ttk.Entry(frame_teacher, textvariable = teacher_password, show="*")
teacher_password_entry.pack()
teacher_button = ttk.Button(frame_teacher, text = 'Login', command = login)
teacher_button.pack()

#Grid
main_frame.columnconfigure(0, weight = 1)
main_frame.columnconfigure(1, weight = 1)
main_frame.rowconfigure(0, weight = 1)

frame_student.grid(row = 0, column = 0)
frame_teacher.grid(row = 0, column = 1)

window.mainloop()