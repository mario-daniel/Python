import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect('rfid')
cursor = conn.cursor()

window = tk.Tk()
window.title('RFID System')
window.geometry('864x576')

class User:
    def __init__(self, first_name = '', last_name = '', user_id = '', password = ''):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.password = password

class Student(User):
    def __init__(self, first_name = '', last_name = '', user_id = '', password = '', grade = ''):
        super().__init__(first_name, last_name, user_id, password)
        self.grade = grade

class Teacher(User):
    def __init__(self, first_name = '', last_name = '', user_id = '', password = '', facility = 0):
        super().__init__(first_name, last_name, user_id, password)
        self.facility = facility

class Card:
    def __init__(self, card_id = 0):
        self.card_id = card_id

def remove_widgets():
    for widget in window.winfo_children():
        widget.destroy()

def login_page():
    def login(Id, password):
        cursor.execute('SELECT password FROM User WHERE user_id = ?', (Id.get(),))
        password_db = cursor.fetchall()
        cursor.execute('SELECT user_id FROM User WHERE user_id = ?', (Id.get(),))
        Id_db = cursor.fetchall()
        if Id_db == [] or password_db == []:
            messagebox.showerror("Login Failed", "User does not exist")
        elif password.get() == password_db[0][0]:
            cursor.execute('SELECT first_name, last_name FROM User WHERE user_id = ?', (Id.get(),))
            name = cursor.fetchall()
            messagebox.showinfo('Login Successful', f'Welcome, {name[0][0]} {name[0][1]}')
            if Id_db[0][0][0] == 'S':
                cursor.execute('SELECT class_grade FROM User WHERE user_id = ?', (Id.get(),))
                grade = cursor.fetchall()
                user = Student(name[0][0], name[0][1], Id_db[0][0], password_db[0][0], grade[0][0])
            else:
                cursor.execute('SELECT facility FROM User WHERE user_id = ?', (Id.get(),))
                facility = cursor.fetchall()
                user = Teacher(name[0][0], name[0][1], Id_db[0][0], password_db[0][0], facility[0][0])
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    #Vairables
    Id = tk.StringVar()
    password = tk.StringVar()

    # main_frames
    main_frame = ttk.Frame(window, width = 864, height = 576)
    main_frame.pack(expand = True, fill = 'both')
    main_frame_login = ttk.Frame(main_frame)

    #Widgets
    ttk.Label(main_frame_login, text = 'ID').pack()
    ttk.Entry(main_frame_login, textvariable = Id).pack()
    ttk.Label(main_frame_login, text = 'Password').pack()
    ttk.Entry(main_frame_login, textvariable = password, show = '*').pack()
    ttk.Button(main_frame_login, text = 'Login', command = lambda: login(Id, password)).pack()
    ttk.Button(main_frame_login, text = "Don't have an account? Register Here!", command = lambda: register_page()).pack()

    #Grid
    main_frame.columnconfigure(0, weight = 1)
    main_frame.columnconfigure(1, weight = 1)
    main_frame.columnconfigure(2, weight = 1)
    main_frame.rowconfigure(0, weight = 1)
    main_frame_login.grid(row = 0, column = 0)

def register_page():
    def register(user_id, password, first_name, last_name, class_grade, facility):
        import re
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        cursor.execute('SELECT user_id FROM User WHERE user_id = ?', (user_id.get(),))
        Id_db = cursor.fetchall()
        if user_id.get() == '' or password.get() == '' or first_name.get() == '' or last_name.get() == '' or (class_grade.get() == '' and facility.get() == ''):
            messagebox.showerror("Register Failed", "All fields must be filled out.")
        elif user_id.get()[0] != 'S' and user_id.get()[0] != 'T':
            messagebox.showerror("Register Failed", "ID can only start with S or T.")
        elif Id_db == user_id.get():
            messagebox.showerror("Register Failed", "User already exists.")
        
        elif not re.match(pattern, password.get()):
            messagebox.showerror("Register Failed", "Password is not strong enough. Please include: 8 Characters minimum, A capital letter, A small letter, A number, A symbol.")

    #Clear Page
    remove_widgets()

    #Vairables
    user_id = tk.StringVar()
    password = tk.StringVar()
    first_name = tk.StringVar()
    last_name = tk.StringVar()
    class_grade = tk.StringVar()
    facility = tk.StringVar()
    class_facility_bool = tk.BooleanVar()
    facilities = ('Football', 'Sixth Form Room', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')
    classes = ('9A', '9B', '9C', '9D', '10A', '10B', '10C', '10D', '11A', '11B', '11C', '11D', '12A', '12B', '12C', '12D', '13A', '13B', '13C', '13D')

    def student_or_teacher():
        if class_facility_bool.get():
            facility_combobox.config(state='disabled')
            grade_class_combobox.config(state='active')
        else:
            grade_class_combobox.config(state='disabled')
            facility_combobox.config(state='active')

    #Frames
    main_frame = ttk.Frame(window, width = 864, height = 576)
    main_frame.pack(expand = True, fill = 'both')

    #Widgets
    ttk.Radiobutton(main_frame, text = 'Student', variable = class_facility_bool, value = True, command = student_or_teacher).pack()
    ttk.Radiobutton(main_frame, text = 'Teacher', variable = class_facility_bool, value = False, command = student_or_teacher).pack()

    ttk.Label(main_frame, text = 'Enter User ID').pack()
    ttk.Entry(main_frame, textvariable = user_id).pack()
    ttk.Label(main_frame, text = 'Enter Password').pack()
    ttk.Entry(main_frame, textvariable = password, show = '*').pack()
    ttk.Label(main_frame, text = 'Enter First Name').pack()
    ttk.Entry(main_frame, textvariable = first_name).pack()
    ttk.Label(main_frame, text = 'Enter Last Name').pack()
    ttk.Entry(main_frame, textvariable = last_name).pack()

    ttk.Label(main_frame, text = 'Choose Class').pack()
    grade_class_combobox = ttk.Combobox(main_frame, state = 'disabled', textvariable = class_grade, values = classes)
    grade_class_combobox.pack()

    ttk.Label(main_frame, text = 'Choose Facility').pack()
    facility_combobox = ttk.Combobox(main_frame, state = 'disabled', textvariable = facility, values = facilities)
    facility_combobox.pack()

    ttk.Button(main_frame, text = 'Register', command = lambda: register(user_id, password, first_name, last_name, class_grade, facility)).pack()

def main():
    login_page()

if __name__ == '__main__':
    main()
    window.mainloop()
