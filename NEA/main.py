import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect('rfid')
cursor = conn.cursor()

window = tk.Tk()
window.title('RFID System')
window.geometry('400x200')

class Login_Main_Screen:
    def __init__(self, window):
        #Vairables
        self.student_id = tk.StringVar()
        self.student_password = tk.StringVar()
        self.teacher_id = tk.StringVar()
        self.teacher_password = tk.StringVar()

        # Frames
        self.main_frame = ttk.Frame(window, width = 400, height = 200)
        self.main_frame.pack(expand = True, fill = 'both')
        self.frame_student = ttk.Frame(self.main_frame, borderwidth = 10, relief = tk.GROOVE)
        self.frame_teacher = ttk.Frame(self.main_frame, borderwidth = 10, relief = tk.GROOVE)

        #Widgets
        self.student_id_label = ttk.Label(self.frame_student, text = 'Student ID')
        self.student_id_label.pack()
        self.student_id_entry = ttk.Entry(self.frame_student, textvariable = self.student_id)
        self.student_id_entry.pack()
        self.student_password_label = ttk.Label(self.frame_student, text = 'Password')
        self.student_password_label.pack()
        self.student_password_entry = ttk.Entry(self.frame_student, textvariable = self.student_password, show = '*')
        self.student_password_entry.pack()
        self.student_button = ttk.Button(self.frame_student, text = 'Login', command = self.login)
        self.student_button.pack()

        self.teacher_id_label = ttk.Label(self.frame_teacher, text = 'Teacher ID')
        self.teacher_id_label.pack()
        self.teacher_id_entry = ttk.Entry(self.frame_teacher, textvariable = self.teacher_id)
        self.teacher_id_entry.pack()
        self.teacher_password_label = ttk.Label(self.frame_teacher, text = 'Password')
        self.teacher_password_label.pack()
        self.teacher_password_entry = ttk.Entry(self.frame_teacher, textvariable = self.teacher_password, show = '*')
        self.teacher_password_entry.pack()
        self.teacher_button = ttk.Button(self.frame_teacher, text = 'Login', command = self.login)
        self.teacher_button.pack()

        self.student_register = ttk.Button(self.frame_student, text = "Don't have an account? Register Here!", command = self.next_page)
        self.student_register.pack()
        self.teacher_register = ttk.Button(self.frame_teacher, text = "Don't have an account? Register Here!", command = self.next_page)
        self.teacher_register.pack()

        #Grid
        self.main_frame.columnconfigure(0, weight = 1)
        self.main_frame.columnconfigure(1, weight = 1)
        self.main_frame.rowconfigure(0, weight = 1)
        self.frame_student.grid(row = 0, column = 0)
        self.frame_teacher.grid(row = 0, column = 1)

    def next_page(self):
        self.main_frame.pack_forget()
        if self.student_register:
            Register_Screen(window, self.student_register)
        elif self.student_register:
            Register_Screen(window, self.teacher_register)

    def login(self):
        if self.student_button:
            cursor.execute('SELECT password FROM Student WHERE student_id = ?', (self.student_id.get(),))
            password_db = cursor.fetchall()
            cursor.execute('SELECT student_id FROM Student WHERE student_id = ?', (self.student_id.get(),))
            student_id_db = cursor.fetchall()
            if student_id_db == [] or password_db == []:
                messagebox.showerror("Login Failed", "User does not exist")
            elif self.student_password.get() == password_db[0][0]:
                cursor.execute('SELECT first_name, last_name FROM Student WHERE student_id = ?', (self.student_id.get(),))
                name = cursor.fetchall()
                messagebox.showinfo('Login Successful', f'Welcome, {name[0][0]} {name[0][1]}')
            else:
                messagebox.showerror("Login Failed", "Incorrect username or password")
        elif self.teacher_button:
            cursor.execute('SELECT password FROM Teacher WHERE teacher_id = ?', (self.teacher_id.get(),))
            password_db = cursor.fetchall()
            cursor.execute('SELECT teacher_id FROM Teacher WHERE teacher_id = ?', (self.teacher_id.get(),))
            teacher_id_db = cursor.fetchall()
            if teacher_id_db == [] or password_db == []:
                messagebox.showerror("Login Failed", "User does not exist")
            elif self.teacher_password.get() == password_db[0][0]:
                cursor.execute('SELECT first_name, last_name FROM Teacher WHERE teacher_id = ?', (self.teacher_id.get(),))
                name = cursor.fetchall()
                messagebox.showinfo('Login Successful', f'Welcome, {name[0][0]} {name[0][1]}')
            else:
                messagebox.showerror("Login Failed", "Incorrect username or password")

class Register_Screen:
    def __init__(self, window, student_register = False, teacher_register = False):

        #Vairables
        self.student_id = tk.StringVar()
        self.student_password = tk.StringVar()
        self.student_first_name = tk.StringVar()
        self.student_last_name = tk.StringVar()
        self.grade_class = tk.StringVar()

        self.teacher_id = tk.StringVar()
        self.teacher_password = tk.StringVar()
        self.teacher_first_name = tk.StringVar()
        self.teacher_last_name = tk.StringVar()
        self.facility = tk.StringVar()

        # Frames
        self.main_frame = ttk.Frame(window, width = 400, height = 400)
        self.main_frame.pack(expand = True, fill = 'both')

        #Widgets
        if student_register:
            self.student_id_label = ttk.Label(self.main_frame, text = 'Enter Student ID')
            self.student_id_label.pack()
            self.student_id_entry = ttk.Entry(self.main_frame, textvariable = self.student_id)
            self.student_id_entry.pack()
            self.student_password_label = ttk.Label(self.main_frame, text = 'Enter Password')
            self.student_password_label.pack()
            self.student_password_entry = ttk.Entry(self.main_frame, textvariable = self.student_password, show = '*')
            self.student_password_entry.pack()
            self.student_first_name_label = ttk.Label(self.main_frame, text = 'Enter First Name')
            self.student_first_name_label.pack()
            self.student_first_name_entry = ttk.Entry(self.main_frame, textvariable = self.student_first_name)
            self.student_first_name_entry.pack()
            self.student_last_name_label = ttk.Label(self.main_frame, text = 'Enter last Name')
            self.student_last_name_label.pack()
            self.student_last_name_entry = ttk.Entry(self.main_frame, textvariable = self.student_last_name)
            self.student_last_name_entry.pack()
            self.student_grade_class_label = ttk.Label(self.main_frame, text = 'Enter Class')
            self.student_grade_class_label.pack()
            self.student_grade_class_entry = ttk.Entry(self.main_frame, textvariable = self.grade_class)
            self.student_grade_class_entry.pack()
            self.student_submit = ttk.Button(self.main_frame, text = 'Register', command = self.register)
            self.student_submit.pack()
        elif teacher_register:
            self.teacher_id_label = ttk.Label(self.main_frame, text = 'Enter Teacher ID')
            self.teacher_id_label.pack()
            self.teacher_id_entry = ttk.Entry(self.main_frame, textvariable = self.teacher_id)
            self.teacher_id_entry.pack()
            self.teacher_password_label = ttk.Label(self.main_frame, text = 'Enter Password')
            self.teacher_password_label.pack()
            self.teacher_password_entry = ttk.Entry(self.main_frame, textvariable = self.teacher_password, show = '*')
            self.teacher_password_entry.pack()
            self.teacher_first_name_label = ttk.Label(self.main_frame, text = 'Enter First Name')
            self.teacher_first_name_label.pack()
            self.teacher_first_name_entry = ttk.Entry(self.main_frame, textvariable = self.teacher_first_name)
            self.teacher_first_name_entry.pack()
            self.teacher_last_name_label = ttk.Label(self.main_frame, text = 'Enter last Name')
            self.teacher_last_name_label.pack()
            self.teacher_last_name_entry = ttk.Entry(self.main_frame, textvariable = self.teacher_last_name)
            self.teacher_last_name_entry.pack()
            self.teacher_facility_label = ttk.Label(self.main_frame, text = 'Enter Facility')
            self.teacher_facility_label.pack()
            self.teacher_facility_entry = ttk.Entry(self.main_frame, textvariable = self.facility)
            self.teacher_facility_entry.pack()
            self.teacher_submit = ttk.button(self.main_frame, text = 'Register', command = self.register)
            self.teacher_submit.pack()

    def register(self):
        if self.student_register:
            cursor.execute('''INSERT INTO Student (
                        student_id, 
                        password, 
                        first_name, 
                        last_name, 
                        class) VALUES (?, ?, ?, ?, ?)''', (
                        self.student_id.get(), 
                        self.student_password.get(), 
                        self.student_first_name.get(), 
                        self.student_last_name.get(), 
                        self.grade_class.get()))
            conn.commit()
        elif self.teacher_register:
            cursor.execute('''INSERT INTO Student (
                        teacher_id, 
                        password, 
                        first_name, 
                        last_name, 
                        facility_id) VALUES (?, ?, ?, ?, ?)''', (
                        self.teacher_id.get(), 
                        self.teacher_password.get(), 
                        self.teacher_first_name.get(), 
                        self.teacher_last_name.get(), 
                        self.facility.get()))
            conn.commit()

main = Login_Main_Screen(window)

window.mainloop()
