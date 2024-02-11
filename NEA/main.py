import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
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

    def login(self, Id, password):
        user_db = cursor.execute('SELECT * FROM User WHERE user_id = ?', (Id.get(),)).fetchall()
        if user_db == []:
            messagebox.showerror("Login Failed", "User does not exist")
        elif self.password_check(user_db, password):
            tag_id_db = cursor.execute('SELECT Card.tag_id, Card.owner FROM Card, User WHERE User.user_id = ? AND User.card_id = Card.card_id;', (user_db[0][0],)).fetchall()
            messagebox.showinfo('Login Successful', f'Welcome, {user_db[0][3]} {user_db[0][4]}')
            if user_db[0][0][0] == 'S':
                return Card(user_db[0][1], tag_id_db[0][0], tag_id_db[0][1]), Student(user_db[0][3], user_db[0][4], user_db[0][0], user_db[0][5], user_db[0][6], user_db[0][7])
            else:
                return Card(user_db[0][1], tag_id_db[0][0], tag_id_db[0][1]), Teacher(user_db[0][3], user_db[0][4], user_db[0][0], user_db[0][5], user_db[0][6], user_db[0][2])
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def password_check(self, user_db, password):
        import hashlib
        salted_password = password.get().encode('utf-8') + user_db[0][6]
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        if hashed_password == user_db[0][5]: return True
        else: return False

    def register(self, user_id, password, first_name, last_name, class_grade, facility, facility_combobox, grade_class_combobox):
        import re
        state = facility_combobox['state'].string
        state2 = grade_class_combobox['state'].string
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        Id_db = cursor.execute('SELECT user_id FROM User WHERE user_id = ?', (user_id.get(),)).fetchall()
        if user_id.get() == '' or password.get() == '' or first_name.get() == '' or last_name.get() == '' or (class_grade.get() == '' and facility.get() == ''):
            messagebox.showerror("Register Failed", "All fields must be filled out.")
        elif user_id.get()[0] != 'S' and user_id.get()[0] != 'T':
            messagebox.showerror("Register Failed", "ID can only start with S or T.")
        elif (user_id.get()[0] == 'S' and state == 'active') or (user_id.get()[0] == 'T' and state2 == 'active'):
            messagebox.showerror("Register Failed", "Teacher or Student can not be responsible for a Class or Facility, Respectively.")
        elif Id_db != []:
            if Id_db[0][0] == user_id.get():
                messagebox.showerror("Register Failed", "User already exists.")
        elif not re.match(pattern, password.get()):
            messagebox.showerror("Register Failed", "Password is not strong enough. Please include: 8 Characters minimum, A capital letter, A small letter, A number, A symbol.")
        elif re.match(pattern, password.get()):
            password = password.get()
            hashed_password, salt = self.password_hash(password)
            facility_id_db = cursor.execute('SELECT facility_id FROM Facility WHERE facility_name = ?', (facility.get(), )).fetchall()
            if facility_id_db == []: facility_id_db = [(0,)]
            card = cursor.execute('SELECT card_id FROM Card WHERE owner IS NULL LIMIT 1;').fetchall()
            if state == 'active':
                cursor.execute('UPDATE Card SET owner = "T" WHERE card_id = ?;', (card[0][0],))
            else:
                cursor.execute('UPDATE Card SET owner = "S" WHERE card_id = ?;', (card[0][0],))
            cursor.execute('INSERT INTO User (user_id, card_id, facility_id, first_name, last_name, hashed_password, salt, class_grade) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id.get(), card[0][0], facility_id_db[0][0], first_name.get(), last_name.get(), hashed_password, salt, class_grade.get()))
            conn.commit()
            messagebox.showinfo('Registration Successful', 'Please Login')
            return True
    
    def password_hash(self, password):
        import hashlib
        import secrets
        salt = secrets.token_bytes(16)
        salted_password = password.encode('utf-8') + salt
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        return hashed_password, salt

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
        self.day = day.get()
        today = datetime.today()
        Day_num = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4}
        days_delta = (Day_num[self.day] - today.weekday()) % 7
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

    def request_problem(self, text_box, problem, problem_combobox, facility):
        other_problem = text_box.get(1.0, "end-1c")
        if facility.get() != '' or other_problem != '':
            problem_state = problem_combobox['state'].string
            facility_id_db = cursor.execute('SELECT facility_id FROM Facility WHERE facility_name = ?;', (facility.get(),)).fetchall()
            if problem_state == 'normal':
                issue_id_db = cursor.execute('SELECT issue_id FROM Issue WHERE issue = ?;', (problem.get(),)).fetchall()
                cursor.execute('INSERT INTO IssueRequest (issue_id, facility_id, resolved) VALUES (?, ?, FALSE);', (issue_id_db[0][0], facility_id_db[0][0]))
                conn.commit()
                
            else:
                cursor.execute('INSERT INTO IssueRequest (issue_id, facility_id, other_issue_reason, resolved) VALUES (0, ?, ?, FALSE);', (facility_id_db[0][0], other_problem))
                conn.commit()
            messagebox.showinfo('Request Successful', 'Your issue will be fixed.')
        else:
            messagebox.showerror("Request Failed", "All fields must be filled out.")

class Teacher(User):
    def __init__(self, first_name = '', last_name = '', user_id = '', hashed_password = '', salt = '', facility = 0):
        super().__init__(first_name, last_name, user_id,  hashed_password, salt)
        self.facility = facility

class Card:
    def __init__(self, card_id = 0, tag_id = '', owner = ''):
        self.card_id = card_id
        self.tag_id = tag_id
        self.owner = owner

class Outgoing_Approval_Segment(ttk.Frame):
    def __init__(self, parent, booking, status, outgoing_approvals):
        super().__init__(master = parent)
        self.booking = booking
        self.outgoing_approvals = outgoing_approvals
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1)
        ttk.Label(self, text = self.booking[1], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 0)
        ttk.Label(self, text = self.booking[2], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 1)
        ttk.Label(self, text = self.booking[3], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 2)
        ttk.Label(self, text = self.booking[4], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 3)
        ttk.Label(self, text = self.booking[5], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 4)
        ttk.Label(self, text = status, width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 5)
        ttk.Button(self, text = 'Remove', command = lambda: self.remove_booking()).grid(row = 0, column = 6)
        self.pack()
    
    def remove_booking(self):
        cursor.execute('UPDATE Timeslot SET status = FALSE WHERE timeslot_id = ?', (self.booking[7],))
        cursor.execute('DELETE FROM Booking WHERE booking_number = ?', (self.booking[0],))
        conn.commit()
        for approval in self.outgoing_approvals: 
            if approval.booking[0] == self.booking[0]:
                for widget in approval.winfo_children():
                    widget.destroy()
                self.outgoing_approvals.remove(approval)
                del approval

class Incoming_Approval_Segment(ttk.Frame):
    def __init__(self, parent, incoming_approvals, booking, card):
        super().__init__(master = parent)
        self.card = card
        self.incoming_approvals = incoming_approvals
        self.booking = booking
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight = 1)
        ttk.Label(self, text = self.booking[8], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 0)
        ttk.Label(self, text = self.booking[9], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 1)
        ttk.Label(self, text = self.booking[10], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 2)
        ttk.Label(self, text = self.booking[1], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 3)
        ttk.Label(self, text = self.booking[2], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 4)
        ttk.Label(self, text = self.booking[3], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 5)
        ttk.Label(self, text = self.booking[4], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 6)
        ttk.Label(self, text = self.booking[5], width = 10, borderwidth = 10, anchor="center", justify="center", relief = tk.GROOVE).grid(row = 0, column = 7)
        ttk.Button(self, text = 'Accept', command = lambda: self.accept_booking()).grid(row = 0, column = 8)
        ttk.Button(self, text = 'Decline', command = lambda: self.decline_booking()).grid(row = 0, column = 9)
        self.pack()

    def accept_booking(self):
        card_id_db = cursor.execute('SELECT card_id FROM User WHERE user_id = ?', (self.booking[11],)).fetchall()
        cursor.execute('UPDATE Timeslot SET status = TRUE, card_id = ? WHERE timeslot_id = ?', (card_id_db[0][0], self.booking[7]))
        cursor.execute('UPDATE Booking SET approved = TRUE WHERE booking_number = ?', (self.booking[0],))
        conn.commit()
        for approval in self.incoming_approvals: 
            if approval.booking[0] == self.booking[0]:
                for widget in approval.winfo_children():
                    widget.destroy()
                self.incoming_approvals.remove(approval)
                del approval

    def decline_booking(self):
        cursor.execute('UPDATE Timeslot SET status = FALSE WHERE timeslot_id = ?', (self.card.card_id,))
        cursor.execute('UPDATE Booking SET approved = FALSE WHERE booking_number = ?', (self.booking[0]))
        conn.commit()
        for approval in self.incoming_approvals: 
            if approval.booking[0] == self.booking[0]:
                for widget in approval.winfo_children():
                    widget.destroy()
                self.incoming_approvals.remove(approval)
                del approval

def remove_widgets():
    #Removes every widget on the page by cyclying through them and destroying them
    for widget in window.winfo_children():
        widget.destroy()

def login_page():

    def login(Id, password):
        card, user = User().login(Id, password)
        if user != None: home_page(user, card)

    #Clear Page
    remove_widgets()

    #Vairables
    Id = tk.StringVar()
    password = tk.StringVar()

    password_icon = (Image.open("padlock.png")).resize((20,20), Image.ADAPTIVE)
    password_icon = ImageTk.PhotoImage(password_icon)
    id_icon = (Image.open("id.png")).resize((20,20), Image.ADAPTIVE)
    id_icon = ImageTk.PhotoImage(id_icon)
    
    #Frames
    login_frame = tk.Frame(window, width = '500', height = '500', highlightbackground="black", highlightthickness=2)
    login_frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

    #Widgets
    window.configure(bg = '#ff7e75')
    ttk.Label(login_frame, text = 'User Login', font = 'Impact 50').place(anchor = 'center', relx = 0.5, rely = 0.25)
    ttk.Label(login_frame, image = id_icon).place(anchor = 'center', relx = 0.3, rely = 0.4)
    ttk.Label(login_frame, text = 'User ID', font = 'Impact 15').place(anchor = 'center', relx = 0.39, rely = 0.4)
    ttk.Entry(login_frame, textvariable = Id, width = 36).place(anchor = 'center', relx = 0.5, rely = 0.45)
    ttk.Label(login_frame, image = password_icon).place(anchor = 'center', relx = 0.3, rely = 0.53)
    ttk.Label(login_frame, text = 'Password', font = 'Impact 15').place(anchor = 'center', relx = 0.41, rely = 0.53)
    ttk.Entry(login_frame, textvariable = password, show = '*', width = 36).place(anchor = 'center', relx = 0.5, rely = 0.58)
    tk.Button(login_frame, text = 'Login', command = lambda: login(Id, password), font = 'Impact', width = 36).place(anchor = 'center', relx = 0.5, rely = 0.7)
    tk.Button(login_frame, bg = '#d4d4d4', text = "Don't have an account? Register Here", command = lambda: register_page()).place(anchor = 'center', relx = 0.5, rely = 0.8)
    window.mainloop()

def register_page(): 

    def register(user_id, password, first_name, last_name, class_grade, facility, facility_combobox, grade_class_combobox):
        if User().register(user_id, password, first_name, last_name, class_grade, facility, facility_combobox, grade_class_combobox): login_page()

    def student_or_teacher():
        if class_facility_bool.get():
            facility_combobox.config(state = 'disabled')
            grade_class_combobox.config(state = 'readonly')
        else:
            grade_class_combobox.config(state = 'disabled')
            facility_combobox.config(state = 'readonly')

    #Clear Page
    remove_widgets()

    #Variables
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
    main_frame = ttk.Frame(window, width = 900, height = 600)
    main_frame.pack()
    login_frame = tk.Frame()
    login_frame.place(anchor = 'center', relx = 0.5, rely = 0.4)

    #Grid
    login_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1)
    login_frame.columnconfigure((0, 1), weight = 1)

    #Widgets
    ttk.Label(login_frame, text = 'First Name', anchor = 'w', justify = 'left', width = 20, font = 'Impact 15').grid(column = 0, row = 0)
    ttk.Entry(login_frame, textvariable = first_name, width = 36).grid(column = 0, row = 1)
    ttk.Label(login_frame, text = 'Last Name', anchor = 'w', justify = 'left', width = 20, font = 'Impact 15').grid(column = 1, row = 0)
    ttk.Entry(login_frame, textvariable = last_name, width = 36).grid(column = 1, row = 1)
    ttk.Label(login_frame, text = 'User ID', anchor = 'w', justify = 'left', width = 20, font = 'Impact 15').grid(column = 0, row = 2)
    ttk.Entry(login_frame, textvariable = user_id, width = 36).grid(column = 0, row = 3)
    ttk.Label(login_frame, text = 'Password', anchor = 'w', justify = 'left', width = 20, font = 'Impact 15').grid(column = 1, row = 2)
    ttk.Entry(login_frame, textvariable = password, width = 36).grid(column = 1, row = 3)
    
    ttk.Label(login_frame, text = 'Class', anchor = 'w', justify = 'left', width = 20, font = 'Impact 15').grid(column = 0, row = 4)
    ttk.Radiobutton(login_frame, text = 'Student', variable = class_facility_bool, value = True, command = student_or_teacher).grid(column = 0, row = 6)
    ttk.Label(login_frame, text = 'Facility', anchor = 'w', justify = 'left', width = 20, font = 'Impact 15').grid(column = 1, row = 4)
    ttk.Radiobutton(login_frame, text = 'Teacher', variable = class_facility_bool, value = False, command = student_or_teacher).grid(column = 1, row = 6)

    grade_class_combobox = ttk.Combobox(login_frame, state = 'disabled', textvariable = class_grade, values = classes, width = 33)
    grade_class_combobox.grid(column = 0, row = 5)

    facility_combobox = ttk.Combobox(login_frame, state = 'disabled', textvariable = facility, values = facilities, width = 33)
    facility_combobox.grid(column = 1, row = 5)

    tk.Button(main_frame, text = 'Register', command = lambda: register(user_id, password, first_name, last_name, class_grade, facility, facility_combobox, grade_class_combobox)).place(anchor = 'center', relx = 0.5, rely = 0.6)
    ttk.Button(main_frame, text = '<--- Login', command = lambda: login_page()).place(anchor = 'center', relx = 0.1, rely = 0.1)

def home_page(user, card):
    #Clear Page
    remove_widgets()
    
    #Frames
    main_frame = ttk.Frame(window, width = 900, height = 600)
    main_frame.pack(expand = True, fill = 'both')

    #Widgets
    ttk.Button(main_frame, text = 'Profile', command = lambda: print('Profile Page')).pack()

    if user.user_id[0] == 'S':
        ttk.Button(main_frame, text = 'Booking History and Support', command = lambda: booking_history_support(user)).pack()
        ttk.Button(main_frame, text = 'Approval Request and Outgoing Approvals', command = lambda: approval_request_page(user, card)).pack()
        ttk.Button(main_frame, text = 'My Analytics', command = lambda: print('My Analytics Page')).pack()
    else:
        ttk.Button(main_frame, text = 'Response History', command = lambda: print('Response History')).pack()
        ttk.Button(main_frame, text = 'Approval Management', command = lambda: approval_management_page(user, card)).pack()
        ttk.Button(main_frame, text = 'School Analytics', command = lambda: print('Analytics Page')).pack()

def approval_request_page(user, card): 

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
        for widget in outgoing_approval_frame.winfo_children():
            widget.destroy()
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
            approval = Outgoing_Approval_Segment(outgoing_approval_frame, booking, status, outgoing_approvals)
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
    outgoing_approval_frame = ttk.Frame(window, borderwidth = 10, relief = tk.GROOVE)
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
    ttk.Button(main_frame, text = 'Refresh', command = lambda: display_outgoing_approvals(user, outgoing_approval_frame)).pack()
    ttk.Button(main_frame, text = '<--- HOME', command = lambda: home_page(user, card)).pack()
    #ttk.Button(main_frame, text = 'Refresh', command = lambda: refresh_window(outgoing_approval_frame)).pack()
    display_outgoing_approvals(user, outgoing_approval_frame)

def approval_management_page(user, card):

    def display_incoming_approvals(user, incoming_approval_frame, card):
        for widget in incoming_approval_frame.winfo_children():
            widget.destroy()
        bookings = cursor.execute('''SELECT Booking.booking_number, Facility.facility_name, Timeslot.start_time, Timeslot.end_time, Timeslot.day, Booking.booking_date, Booking.approved, Booking.timeslot_id, User.first_name, User.last_name, User.class_grade, User.user_id
                                    FROM Facility, Timeslot, Booking, User
                                    WHERE Booking.facility_id = Facility.facility_id
                                    AND Booking.approved IS NULL
                                    AND Booking.facility_id = ?
                                    AND Booking.timeslot_id = Timeslot.timeslot_id
                                    AND User.user_id = Booking.user_id;''', (user.facility,)).fetchall()
        incoming_approvals = []
        for booking in bookings:
            if booking[6] == None: status = 'Pending'
            elif booking[6] == 1: status = 'Approved'
            else: status = 'Declined'
            approval = Incoming_Approval_Segment(incoming_approval_frame, incoming_approvals, booking, card)
            incoming_approvals.append(approval)

    #Clear Page
    remove_widgets()

    #Frames
    main_frame = ttk.Frame(window, width = 900, height = 600)
    main_frame.pack(expand = True, fill = 'both')
    incoming_approval_frame = ttk.Frame(window, width = 900, height = 300, borderwidth = 10, relief = tk.GROOVE)
    incoming_approval_frame.pack(expand = True, fill = 'both')

    #Widgets
    ttk.Label(main_frame, text = 'Approval Request').pack()
    display_incoming_approvals(user, incoming_approval_frame, card)

def booking_history_support(user):

    def choose_or_other():
        if other_bool.get():
            text_box.config(state = 'normal')
            problem_combobox.config(state = 'disabled')
        else:
            text_box.config(state = 'disabled')
            problem_combobox.config(state = 'active')

    #Clear Page
    remove_widgets()

    #Variables
    problem = tk.StringVar()
    facility = tk.StringVar()
    other_bool = tk.BooleanVar()
    problems = ['Facility Damage', 'Facility Resources Empty', 'Theft of Facility Equipment', 'Health Hazard']
    facilities = ('Football', 'Sixth Form Room', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')


    #Frames
    main_frame = ttk.Frame(window, width = 900, height = 600)
    main_frame.pack(expand = True, fill = 'both')
    selection_frame = ttk.Frame(main_frame)

    #Grid
    selection_frame.rowconfigure(0, weight = 1)
    selection_frame.columnconfigure((0, 1), weight = 1)    

    #Widgets
    ttk.Label(main_frame, text = 'Request Problem').pack()
    ttk.Combobox(main_frame, textvariable = facility, values = facilities).pack()
    selection_frame.pack()
    problem_radiobutton = ttk.Radiobutton(selection_frame, value = False, variable = other_bool, command = lambda: choose_or_other())
    problem_radiobutton.grid(row = 0, column = 0)
    problem_combobox = ttk.Combobox(selection_frame, textvariable = problem, values = problems)
    problem_combobox.grid(row = 0, column = 1)
    other_radiobutton = ttk.Radiobutton(main_frame, text = 'Other', value = True, variable = other_bool, command = lambda: choose_or_other())
    other_radiobutton.pack()
    text_box = tk.Text(main_frame, state = 'disabled')
    text_box.pack()
    submit_button = ttk.Button(main_frame, text = 'Submit', command = lambda: user.request_problem(text_box, problem, problem_combobox, facility))
    submit_button.pack()

if __name__ == '__main__':
    from database_init import main
    main()
    login_page()
    window.mainloop()
