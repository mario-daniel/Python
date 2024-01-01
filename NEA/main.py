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
                self.start_time = f'{timing_format[:index - 1].strip()}:00'
                self.end_time = f'{timing_format[index + 1:].strip()}:00'
        from datetime import datetime, timedelta
        # Get today's date
        self.day = day.get()
        today = datetime.today()
        Day_num = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4}
        # Calculate days until next Day
        days_delta = (Day_num[self.day] - today.weekday()) % 7
        # Calculate the date of the Day
        self.date = (today + timedelta(days=days_delta)).strftime('%Y-%m-%d')
    
    def request(self, day, facility, timing, timings_available_combobox):
        self.get_time(day, timing)
        facility_id_db = cursor.execute('SELECT facility_id FROM Facility WHERE facility_name = ?', (facility.get(), )).fetchall()
        self.timeslot_id_db = cursor.execute('SELECT timeslot_id FROM Timeslot WHERE day = ? AND facility_id = ? AND start_time = ? AND end_time = ?', (self.day, facility_id_db[0][0], self.start_time, self.end_time)).fetchall()
        cursor.execute('INSERT INTO Booking (facility_id, user_id, timeslot_id, booking_date) VALUES (?, ?, ?, ?)', (facility_id_db[0][0], self.user_id, self.timeslot_id_db[0][0], self.date))
        conn.commit()
        self.update_table()
        timing.set('')
        timings_available_combobox.config(state = 'disabled')
        messagebox.showinfo('Request Successful', f'Requested from {self.start_time} to {self.end_time} on {self.day} {self.date}')
    
    def update_table(self):
            cursor.execute('UPDATE Timeslot SET status = NULL WHERE timeslot_id = ?', (self.timeslot_id_db[0][0],))
            conn.commit()

class Teacher(User):
    def __init__(self, first_name = '', last_name = '', user_id = '', hashed_password = '', salt = '', facility = 0):
        super().__init__(first_name, last_name, user_id,  hashed_password, salt)
        self.facility = facility

class Card:
    def __init__(self, card_id = 0):
        self.card_id = card_id

class Outgoing_Approval_Segment(ttk.Frame):
    def __init__(self, parent, booking_number, facility, start_time, end_time, day, date, status, timeslot_id, outgoing_approvals):
        super().__init__(master = parent)
        self.booking_number = booking_number
        self.timeslot_id = timeslot_id
        self.outgoing_approvals = outgoing_approvals
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1)
        ttk.Label(self, text = facility, width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 0)
        ttk.Label(self, text = start_time, width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 1)
        ttk.Label(self, text = end_time, width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 2)
        ttk.Label(self, text = day, width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 3)
        ttk.Label(self, text = date, width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 4)
        ttk.Label(self, text = status, width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 5)
        ttk.Button(self, text = 'Remove', command = lambda: self.remove_booking()).grid(row = 0, column = 6)
        self.pack()
    
    def remove_booking(self):
        cursor.execute('UPDATE Timeslot SET status = FALSE WHERE timeslot_id = ?', (self.timeslot_id,))
        cursor.execute('DELETE FROM Booking WHERE booking_number = ?', (self.booking_number,))
        conn.commit()
        for approval in self.outgoing_approvals: 
            if approval.booking_number == self.booking_number:
                for widget in approval.winfo_children():
                    widget.destroy()
                self.outgoing_approvals.remove(approval)
                del approval

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
                home_page(user)
            else:
                user = Teacher(user_db[0][2], user_db[0][3], user_db[0][0], user_db[0][4], user_db[0][5], user_db[0][1])
                home_page(user)
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
            facility_id_db = cursor.execute('SELECT facility_id FROM Facility WHERE facility_name = ?', (facility.get(), )).fetchall()
            if facility_id_db == []: facility_id_db = [(0,)]
            cursor.execute('INSERT INTO User (user_id, facility_id, first_name, last_name, hashed_password, salt, class_grade) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id.get(), facility_id_db[0][0], first_name.get(), last_name.get(), hashed_password, salt, class_grade.get()))
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
    facilities = ('Football', 'Sixth Form Room', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')
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
    ttk.Entry(main_frame, textvariable = password).pack()
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

def home_page(user):
    #Clear Page
    remove_widgets()
    
    #Frames
    main_frame = ttk.Frame(window, width = 864, height = 576)
    main_frame.pack(expand = True, fill = 'both')

    #Widgets
    ttk.Button(main_frame, text = 'Profile', command = lambda: print('Profile Page')).pack()
    ttk.Button(main_frame, text = 'Bookings', command = lambda: print('Bookings Page')).pack()
    ttk.Button(main_frame, text = 'Analytics', command = lambda: print('Analytics Page')).pack()

    if user.user_id[0] == 'S':
        ttk.Button(main_frame, text = 'Approval Request', command = lambda: approval_request_page(user)).pack()
    else:
        ttk.Button(main_frame, text = 'Approval Management', command = lambda: print('Approval Management Page')).pack()

def approval_request_page(user): 

    def display_timings_available(day, facility, timings_available_combobox):
        timings_available = []
        timings = cursor.execute('''SELECT Timeslot.start_time, Timeslot.end_time 
                                 FROM Timeslot 
                                 JOIN Facility ON Facility.facility_id = Timeslot.facility_id 
                                 WHERE Timeslot.day = ? 
                                    AND Facility.facility_name = ? 
                                    AND Timeslot.status = 0;''' ,(day.get(), facility.get())).fetchall()
        for slot in timings:
            timings_available.append(f'{slot[0][:-3]} - {slot[1][:-3]}')
        timings_available_combobox.config(state = 'active')
        timings_available_combobox.config(values = timings_available)

    def display_outgoing_approvals(user, outgoing_approval_frame):
        bookings = cursor.execute('''SELECT Booking.booking_number, Facility.facility_name, Timeslot.start_time, Timeslot.end_time, Timeslot.day, Booking.booking_date, Booking.approved, Booking.timeslot_id 
                                    FROM Facility, Timeslot, Booking 
                                    WHERE Facility.facility_id = Booking.facility_id
                                        AND Timeslot.timeslot_id = Booking.timeslot_id
                                        AND Booking.user_id = ?;''', (user.user_id,)).fetchall()
        outgoing_approvals = []
        for booking in bookings:
            if booking[6] == None: status = 'Pending'
            elif booking[6] == 1: status = 'Approved'
            else: status = 'Declined'
            approval = Outgoing_Approval_Segment(outgoing_approval_frame, booking[0], booking[1], booking[2], booking[3], booking[4], booking[5], status, booking[7], outgoing_approvals)
            outgoing_approvals.append(approval)

    #Clear Page
    remove_widgets()

    #Variables
    facilities = ('Football', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')
    facility = tk.StringVar()
    day = tk.StringVar()
    timing = tk.StringVar()
    
    #Frames
    main_frame = ttk.Frame(window, width = 900, height = 600)
    main_frame.pack(expand = True, fill = 'both')
    outgoing_approval_frame = ttk.Frame(window, width = 900, height = 300, borderwidth = 10, relief = tk.GROOVE)
    outgoing_approval_frame.pack(expand = True, fill = 'both')

    #Widgets
    ttk.Label(main_frame, text = 'Approval Request').pack()
    ttk.Label(main_frame, text = 'Request a new approval').pack()
    ttk.Label(main_frame, text = 'Pick Facility').pack()
    ttk.Combobox(main_frame, textvariable = facility, values = facilities).pack()
    ttk.Label(main_frame, text = 'Pick Day').pack()
    ttk.Combobox(main_frame, textvariable = day, values = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')).pack()
    ttk.Label(main_frame, text = 'Pick Timing').pack()
    timings_available_combobox = ttk.Combobox(main_frame, state = 'disabled', textvariable = timing, values = [])
    timings_available_combobox.pack()
    ttk.Button(main_frame, text = 'Check Available Timings', command = lambda: display_timings_available(day, facility, timings_available_combobox)).pack()
    ttk.Button(main_frame, text = 'Request', command = lambda: user.request(day, facility, timing, timings_available_combobox)).pack()
    ttk.Button(main_frame, text = 'Check outgoing approvals', command = lambda: display_outgoing_approvals(user, outgoing_approval_frame)).pack()
    ttk.Button(main_frame, text = '<--- Home', command = lambda: home_page(user)).pack()

if __name__ == '__main__':
    login_page()
    window.mainloop()
