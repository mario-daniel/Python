import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect('rfid')
cursor = conn.cursor()

window = tk.Tk()
window.title('RFID System')
window.geometry('900x600')

class User:
    def __init__(self, first_name = '', last_name = '', user_id = '', hashed_password = '', salt = ''):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.hashed_password = hashed_password
        self.salt = salt

class Student(User): 
    def __init__(self, first_name = '', last_name = '', user_id = '', hashed_password = '', salt = '', grade = ''):
        super().__init__(first_name, last_name, user_id,  hashed_password, salt)
        self.grade = grade

    def get_time(self, day, timing):
        timing_format = timing.get()
        for index in range(len(timing_format)):
            if timing_format[index] == '-':
                start_time = f'{timing_format[:index - 1].strip()}:00'
                end_time = f'{timing_format[index + 1:].strip()}:00'
        from datetime import datetime, timedelta
        # Get today's date
        day = day.get()
        today = datetime.today()
        Day_num = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4}
        # Calculate days until next Day
        days_delta = (Day_num[day] - today.weekday()) % 7
        # Calculate the date of the Day
        date = (today + timedelta(days=days_delta)).strftime('%Y-%m-%d')
        start_date_time = f'{start_time} {date}'
        end_date_time = f'{end_time} {date}'
        return start_date_time, end_date_time, date, start_time, end_time, day
    
    def request(self, facilities, day, facility, timing):
        start_date_time, end_date_time, date, start_time, end_time, day = self.get_time(day, timing)
        cursor.execute('INSERT INTO Booking (facility_id, user_id, booking_start_time, booking_end_time) VALUES (?, ?, ?, ?)', (facilities[facility.get()], self.user_id, start_date_time, end_date_time))
        conn.commit()
        messagebox.showinfo('Request Successful', f'Requested from {start_time} to {end_time} on {day} {date}')

class Teacher(User):
    def __init__(self, first_name = '', last_name = '', user_id = '', hashed_password = '', salt = '', facility = 0):
        super().__init__(first_name, last_name, user_id,  hashed_password, salt)
        self.facility = facility

class Card:
    def __init__(self, card_id = 0):
        self.card_id = card_id

class Segment(ttk.Frame):
    def __init__(self, parent, facility, status, start_time, end_time, date):
        super().__init__(master = parent)

def remove_widgets():
    #Removes every widget on the page by cyclying through them and destroying them
    for widget in window.winfo_children():
        widget.destroy()

def login_page():
    #A nested function for the backend checks
    def login(Id, password):
        #Gets the password and user id from the database of the user inputed
        user_db = cursor.execute('SELECT * FROM User WHERE user_id = ?', (Id.get(),)).fetchall()
        #Checks if the user exists or not
        if user_db == []:
            messagebox.showerror("Login Failed", "User does not exist")
        #Checks if the passwords match
        elif password_check(user_db[0][4], Id, password):
            messagebox.showinfo('Login Successful', f'Welcome, {user_db[0][2]} {user_db[0][3]}')
            #Checks whether it is a student or teacher and shows them their respective home page.
            if user_db[0][0][0] == 'S':
                user = Student(user_db[0][2], user_db[0][3], user_db[0][0], user_db[0][4], user_db[0][5], user_db[0][6])
                home_page(user, user_db)
            else:
                user = Teacher(user_db[0][2], user_db[0][3], user_db[0][0], user_db[0][4], user_db[0][5], user_db[0][1])
                home_page(user, user_db)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def password_check(hashed_password_db, Id, password):
        import hashlib

        # Retrieve Salt from database
        salt = cursor.execute('SELECT salt FROM User WHERE user_id = ?', (Id.get(),)).fetchall()

        # Combine the password and salt
        #password = password.get()
        salted_password = password.get().encode('utf-8') + salt[0][0]

        # Create a hashed password to check with the original using SHA256
        hashed_password = hashlib.sha256(salted_password).hexdigest()

        if hashed_password == hashed_password_db: return True
        else: return False

    #Clear Page
    remove_widgets()

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
    #A nested function for the backend checks and registration
    def register(user_id, password, first_name, last_name, class_grade, facility, facilities, facility_combobox, grade_class_combobox):
        import re
        state = facility_combobox['state'].string
        state2 = grade_class_combobox['state'].string
        #Password requirements
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        #Gets user id from database and sets to a variable
        cursor.execute('SELECT user_id FROM User WHERE user_id = ?', (user_id.get(),))
        Id_db = cursor.fetchall()
        #Checks whether all boxes are filled out.
        if user_id.get() == '' or password.get() == '' or first_name.get() == '' or last_name.get() == '' or (class_grade.get() == '' and facility.get() == ''):
            messagebox.showerror("Register Failed", "All fields must be filled out.")
        #Checks whether the first value of the id inputed is an S or T.
        elif user_id.get()[0] != 'S' and user_id.get()[0] != 'T':
            messagebox.showerror("Register Failed", "ID can only start with S or T.")
        #Checks if the the facility or student combobox is filled out when its not their roles respectively.
        elif (user_id.get()[0] == 'S' and state == 'active') or (user_id.get()[0] == 'T' and state2 == 'active'):
            messagebox.showerror("Register Failed", "Teacher or Student can not be responsible for a Class or Facility, Respectively.")
        #Checks if the user is already registered.
        elif Id_db != []:
            if Id_db[0][0] == user_id.get():
                messagebox.showerror("Register Failed", "User already exists.")
        #Checks if the password matches the requirements
        elif not re.match(pattern, password.get()):
            messagebox.showerror("Register Failed", "Password is not strong enough. Please include: 8 Characters minimum, A capital letter, A small letter, A number, A symbol.")
        #Hashes password
        elif re.match(pattern, password.get()):
            password = password.get()
            hashed_password, salt = password_hash(password)
            cursor.execute('INSERT INTO User (user_id, facility_id, first_name, last_name, hashed_password, salt, class_grade) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id.get(), facilities[facility.get()], first_name.get(), last_name.get(), hashed_password, salt, class_grade.get()))
            conn.commit()
            messagebox.showinfo('Registration Successful', 'Please Login')
            login_page()
    #A nested function to hash the password the user inputted.
    def password_hash(password):
        import hashlib
        import secrets

        # Generate a random salt
        salt = secrets.token_bytes(16)

        # Combine the password and salt
        salted_password = password.encode('utf-8') + salt

        # Create a hash using SHA256
        hashed_password = hashlib.sha256(salted_password).hexdigest()

        return hashed_password, salt

    #A nested function to enable and disable the repsective comboboxes of the users' choice
    def student_or_teacher():
        if class_facility_bool.get():
            facility_combobox.config(state='disabled')
            grade_class_combobox.config(state='active')
        else:
            grade_class_combobox.config(state='disabled')
            facility_combobox.config(state='active')

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
    facilities = {'' : 0, 'Football': 1, 'Sixth Form Room': 2, 'Basketball': 3, 'Cricket': 4, 'Multi-Purpose Hall': 5, 'Fitness Suite': 6}
    classes = ('9A', '9B', '9C', '9D', '10A', '10B', '10C', '10D', '11A', '11B', '11C', '11D', '12A', '12B', '12C', '12D', '13A', '13B', '13C', '13D')

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
    facility_combobox = ttk.Combobox(main_frame, state = 'disabled', textvariable = facility, values = ('Football', 'Sixth Form Room', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite'))
    facility_combobox.pack()

    ttk.Button(main_frame, text = 'Register', command = lambda: register(user_id, password, first_name, last_name, class_grade, facility, facilities, facility_combobox, grade_class_combobox)).pack()
    ttk.Button(main_frame, text = '<--- Login', command = lambda: login_page()).pack()

def home_page(user, user_db):
    #Clear Page
    remove_widgets()
    
    #Frames
    main_frame = ttk.Frame(window, width = 864, height = 576)
    main_frame.pack(expand = True, fill = 'both')

    #Widgets
    ttk.Button(main_frame, text = 'Profile', command = lambda: print('Profile Page')).pack()
    ttk.Button(main_frame, text = 'Bookings', command = lambda: print('Bookings Page')).pack()
    ttk.Button(main_frame, text = 'Analytics', command = lambda: print('Analytics Page')).pack()

    if user_db[0][0][0] == 'S':
        ttk.Button(main_frame, text = 'Approval Request', command = lambda: approval_request_page(user)).pack()
    else:
        ttk.Button(main_frame, text = 'Approval Management', command = lambda: print('Approval Management Page')).pack()

def approval_request_page(user):

    def display_timings_available(timing, timings_available_combobox):
        timings_available = []
        if facility.get() != '':
            for facility_dict, days in timetable.items():
                if facility_dict == facility.get():
                    for day_dict, timings in days.items():
                        if day_dict == day.get():
                            for timing in timings:
                                timings_available.append(timing)
        timings_available_combobox.config(state = 'active')
        timings_available_combobox.config(values = timings_available)

    def display_outgoing_approvals(user):
        booking = cursor.execute('SELECT * FROM Booking WHERE user_id = ?', (user.user_id,)).fetchall()
        print(booking)

    #Clear Page
    remove_widgets()

    #Variables
    facilities = {'' : 0, 'Football': 1, 'Sixth Form Room': 2, 'Basketball': 3, 'Cricket': 4, 'Multi-Purpose Hall': 5, 'Fitness Suite': 6}
    facility = tk.StringVar()
    day = tk.StringVar()
    timing = tk.StringVar()
    timetable = {
        'Football': {
            'Monday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Tuesday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Wednesday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Thursday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Friday': ['08:10 - 08:55', '08:55 - 09:40', '09:40 - 10:25', '10:25 - 10:45', '10:45 - 11:30']},
        'Basketball': {
            'Monday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Tuesday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Wednesday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Thursday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Friday': ['08:10 - 08:55', '08:55 - 09:40', '09:40 - 10:25', '10:25 - 10:45', '10:45 - 11:30']},
        'Cricket': {
            'Monday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Tuesday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Wednesday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Thursday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Friday': ['08:10 - 08:55', '08:55 - 09:40', '09:40 - 10:25', '10:25 - 10:45', '10:45 - 11:30']},
        'Multi-Purpose Hall': {
            'Monday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Tuesday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Wednesday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Thursday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Friday': ['08:10 - 08:55', '08:55 - 09:40', '09:40 - 10:25', '10:25 - 10:45', '10:45 - 11:30']},
        'Fitness Suite': {
            'Monday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Tuesday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Wednesday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Thursday': ['07:40 - 08:25', '08:25 - 09:10', '09:10 - 09:55', '09:55 - 10:15', '10:15 - 11:00', '11:00 - 11:45', '11:45 - 12:30', '12:30 - 13:10', '13:10 - 13:55', '13:55 - 14:40'],
            'Friday': ['08:10 - 08:55', '08:55 - 09:40', '09:40 - 10:25', '10:25 - 10:45', '10:45 - 11:30']}
            }

    #Frames
    main_frame = ttk.Frame(window, width = 900, height = 600)
    main_frame.pack(expand = True, fill = 'both')
    outgoing_approval_frame = ttk.Frame(window, width = 900, height = 300)

    #Widgets
    ttk.Label(main_frame, text = 'Approval Request').pack()
    ttk.Label(main_frame, text = 'Request a new approval').pack()
    ttk.Label(main_frame, text = 'Pick Facility').pack()
    ttk.Combobox(main_frame, textvariable = facility, values = ('Football', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')).pack()
    ttk.Label(main_frame, text = 'Pick Day').pack()
    ttk.Combobox(main_frame, textvariable = day, values = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')).pack()
    ttk.Label(main_frame, text = 'Pick Timing').pack()
    timings_available_combobox = ttk.Combobox(main_frame, state = 'disabled', textvariable = timing, values = [])
    timings_available_combobox.pack()
    ttk.Button(main_frame, text = 'Check Available Timings', command = lambda: display_timings_available(timing, timings_available_combobox)).pack()
    ttk.Button(main_frame, text = 'Request', command = lambda: user.request(facilities, day, facility, timing)).pack()
    ttk.Button(main_frame, text = 'Check outgoing approvals', command = lambda: display_outgoing_approvals(user)).pack()

if __name__ == '__main__':
    login_page()
    window.mainloop()
