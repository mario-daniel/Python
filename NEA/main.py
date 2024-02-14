import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3

conn = sqlite3.connect('rfid')
cursor = conn.cursor()

window = ctk.CTk(fg_color = '#ff7e75')
window.title('RFID System')
window.geometry('600x600')
window.resizable(False, False)
# window_frame = ctk.CTkFrame(window, fg_color = '#ff7e75', corner_radius = 0, border_color = 'black', border_width = 2)
# window_frame.pack(expand = True, fill = 'both')
ctk.set_appearance_mode('light')

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

    def register(self, user_id, password, first_name, last_name, class_facility, class_facility_bool):
        import re
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        Id_db = cursor.execute('SELECT user_id FROM User WHERE user_id = ?', (user_id.get(),)).fetchall()
        if user_id.get() == '' or password.get() == '' or first_name.get() == '' or last_name.get() == '' or class_facility.get() == '':
            messagebox.showerror("Register Failed", "All fields must be filled out.")
        elif Id_db != []:
            if Id_db[0][0] == user_id.get():
                messagebox.showerror("Register Failed", "User already exists.")
        elif not re.match(pattern, password.get()):
            messagebox.showerror("Register Failed", "Password is not strong enough. Please include: 8 Characters minimum, A capital letter, A small letter, A number, A symbol.")
        elif re.match(pattern, password.get()):
            password = password.get()
            hashed_password, salt = self.password_hash(password)
            facility_id_db = cursor.execute('SELECT facility_id FROM Facility WHERE facility_name = ?', (class_facility.get(), )).fetchall()
            if facility_id_db == []: facility_id_db = [(0,)]
            card = cursor.execute('SELECT card_id FROM Card WHERE owner IS NULL LIMIT 1;').fetchall()
            if not class_facility_bool.get():
                cursor.execute('UPDATE Card SET owner = "T" WHERE card_id = ?;', (card[0][0],))
                class_grade = ''
                user_id = f'T{user_id.get()}'
            else:
                cursor.execute('UPDATE Card SET owner = "S" WHERE card_id = ?;', (card[0][0],))
                class_grade = class_facility.get()
                user_id = f'S{user_id.get()}'
            cursor.execute('INSERT INTO User (user_id, card_id, facility_id, first_name, last_name, hashed_password, salt, class_grade) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, card[0][0], facility_id_db[0][0], first_name.get(), last_name.get(), hashed_password, salt, class_grade))
            conn.commit()
            messagebox.showinfo('Registration Successful', f'Please Login with {user_id}')
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
        timings_available_combobox.configure(state = 'disabled')
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

class Outgoing_Approval_Segment(ctk.CTkFrame):
    def __init__(self, parent, booking, status, outgoing_approvals):
        super().__init__(master = parent)
        self.booking = booking
        self.outgoing_approvals = outgoing_approvals
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1)
        ctk.CTkLabel(self, text = self.booking[1], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 0)
        ctk.CTkLabel(self, text = self.booking[2], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 1)
        ctk.CTkLabel(self, text = self.booking[3], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 2)
        ctk.CTkLabel(self, text = self.booking[4], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 3)
        ctk.CTkLabel(self, text = self.booking[5], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 4)
        ctk.CTkLabel(self, text = status, width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 5)
        ctk.CTkButton(self, text = 'Remove', command = lambda: self.remove_booking()).grid(row = 0, column = 6)
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

class Incoming_Approval_Segment(ctk.CTkFrame):
    def __init__(self, parent, incoming_approvals, booking, card):
        super().__init__(master = parent)
        self.card = card
        self.incoming_approvals = incoming_approvals
        self.booking = booking
        self.rowconfigureure(0, weight = 1)
        self.columnconfigureure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight = 1)
        ctk.CTkLabel(self, text = self.booking[8], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 0)
        ctk.CTkLabel(self, text = self.booking[9], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 1)
        ctk.CTkLabel(self, text = self.booking[10], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 2)
        ctk.CTkLabel(self, text = self.booking[1], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 3)
        ctk.CTkLabel(self, text = self.booking[2], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 4)
        ctk.CTkLabel(self, text = self.booking[3], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 5)
        ctk.CTkLabel(self, text = self.booking[4], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 6)
        ctk.CTkLabel(self, text = self.booking[5], width = 10, borderwidth = 10, anchor="center", justify="center", relief = ctk.CTkGROOVE).grid(row = 0, column = 7)
        ctk.CTkButton(self, text = 'Accept', command = lambda: self.accept_booking()).grid(row = 0, column = 8)
        ctk.CTkButton(self, text = 'Decline', command = lambda: self.decline_booking()).grid(row = 0, column = 9)
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
    Id = ctk.StringVar()
    password = ctk.StringVar()

    password_icon = ctk.CTkImage(light_image = Image.open("padlock.png"), size = (22,22))
    id_icon = ctk.CTkImage(light_image = Image.open("id.png"), size = (22,22))
    
    #Frames
    login_frame = ctk.CTkFrame(window, width = 500, height = 500, border_color = 'black', border_width = 2, fg_color = '#F0F0F0', corner_radius = 0)
    login_frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

    #Widgets
    ctk.CTkLabel(login_frame, text = 'User Login', font = ('Impact', 70)).place(anchor = 'center', relx = 0.5, rely = 0.25)
    ctk.CTkLabel(login_frame, text = '', image = id_icon).place(anchor = 'center', relx = 0.33, rely = 0.4)
    ctk.CTkLabel(login_frame, text = 'User ID', font = ('Impact', 20)).place(anchor = 'center', relx = 0.42, rely = 0.4)
    ctk.CTkEntry(login_frame, textvariable = Id, width = 200, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.5, rely = 0.45)
    ctk.CTkLabel(login_frame, text = '', image = password_icon).place(anchor = 'center', relx = 0.33, rely = 0.525)
    ctk.CTkLabel(login_frame, text = 'Password', font = ('Impact', 20)).place(anchor = 'center', relx = 0.44, rely = 0.53)
    ctk.CTkEntry(login_frame, textvariable = password, show = '*', width = 200, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.5, rely = 0.58)
    ctk.CTkButton(login_frame, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = 'Login', text_color = 'black', fg_color = 'white', font = ('Impact', 25), command = lambda: login(Id, password)).place(anchor = 'center', relx = 0.5, rely = 0.7)
    ctk.CTkLabel(login_frame, text = 'or').place(anchor = 'center', relx = 0.5, rely = 0.77)
    ctk.CTkButton(login_frame, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Don't have an account? Register Here", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = lambda: register_page()).place(anchor = 'center', relx = 0.5, rely = 0.83)

def register_page(): 

    def register(user_id, password, first_name, last_name, class_facility, class_facility_bool):
        if User().register(user_id, password, first_name, last_name, class_facility, class_facility_bool): login_page()

    def student_or_teacher():
        if class_facility_bool.get():
            Label.configure(text = 'Select Class')
            grade_facility_combobox.configure(values = classes, state = 'readonly')
        else:
            Label.configure(text = 'Select Facility')
            grade_facility_combobox.configure(values = facilities, state = 'readonly')

    #Clear Page
    remove_widgets()

    #Variables
    user_id = ctk.StringVar()
    password = ctk.StringVar()
    first_name = ctk.StringVar()
    last_name = ctk.StringVar()
    class_facility = ctk.StringVar()
    class_facility_bool = ctk.BooleanVar()
    facilities = ('Football', 'Sixth Form Room', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')
    classes = ('9A', '9B', '9C', '9D', '10A', '10B', '10C', '10D', '11A', '11B', '11C', '11D', '12A', '12B', '12C', '12D', '13A', '13B', '13C', '13D')

    #Frames
    login_frame = ctk.CTkFrame(window, width = 500, height = 500, border_color = "black", fg_color = '#F0F0F0', border_width = 2, corner_radius = 0)
    login_frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

    #Widgets
    ctk.CTkLabel(login_frame, text = 'Register', font = ('Impact', 70)).place(anchor = 'center', relx = 0.5, rely = 0.17)
    ctk.CTkLabel(login_frame, text = 'First Name', font = ('Impact', 20)).place(anchor = 'center', relx = 0.2, rely = 0.32)
    ctk.CTkEntry(login_frame, textvariable = first_name, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.3, rely = 0.37)
    ctk.CTkLabel(login_frame, text = 'Last Name', font = ('Impact', 20)).place(anchor = 'center', relx = 0.6, rely = 0.32)
    ctk.CTkEntry(login_frame, textvariable = last_name, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.7, rely = 0.37)
    ctk.CTkLabel(login_frame, text = 'User ID', font = ('Impact', 20)).place(anchor = 'center', relx = 0.18, rely = 0.47)
    ctk.CTkEntry(login_frame, textvariable = user_id, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.3, rely = 0.52)
    ctk.CTkLabel(login_frame, text = 'Password', font = ('Impact', 20)).place(anchor = 'center', relx = 0.2, rely = 0.62)
    ctk.CTkEntry(login_frame, textvariable = password, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.3, rely = 0.67)
    
    ctk.CTkLabel(login_frame, text = 'Occupation', font = ('Impact', 20)).place(anchor = 'center', relx = 0.61, rely = 0.47)
    student_button = ctk.CTkRadioButton(login_frame, text = 'Student', fg_color = 'black', border_color = 'black', hover_color = '#707070', radiobutton_height = 10, radiobutton_width = 10, variable = class_facility_bool, value = True, command = student_or_teacher)
    student_button.place(anchor = 'center', relx = 0.62, rely = 0.52)
    ctk.CTkLabel(login_frame, text = 'Facility', font = ('Impact', 20))
    teacher_button = ctk.CTkRadioButton(login_frame, text = 'Teacher', fg_color = 'black', border_color = 'black', hover_color = '#707070', radiobutton_height = 10, radiobutton_width = 10, variable = class_facility_bool, value = False, command = student_or_teacher)
    teacher_button.place(anchor = 'center', relx = 0.8, rely = 0.52)

    Label = ctk.CTkLabel(login_frame, text = 'Select Occupation', font = ('Impact', 20))
    Label.place(anchor = 'w', relx = 0.51, rely = 0.62)
    grade_facility_combobox = ctk.CTkComboBox(login_frame, border_color = 'black', button_color = 'black', state = 'disabled', variable = class_facility, values = '', width = 190, dropdown_font = ('Impact', 15))
    grade_facility_combobox.place(anchor = 'center', relx = 0.7, rely = 0.67)

    ctk.CTkButton(login_frame, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Register", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = lambda: register(user_id, password, first_name, last_name, class_facility, class_facility_bool)).place(anchor = 'center', relx = 0.5, rely = 0.79)
    ctk.CTkLabel(login_frame, text = 'or').place(anchor = 'center', relx = 0.5, rely = 0.86)
    ctk.CTkButton(login_frame, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Login", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = lambda: login_page()).place(anchor = 'center', relx = 0.5, rely = 0.92)

def home_page(user, card):
    #Clear Page
    remove_widgets()
    
    #Frames
    login_frame = ctk.CTkFrame(window, width = 500, height = 500, border_color = "black", border_width = 2)
    login_frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

    #Widgets
    ctk.CTkButton(login_frame, text = 'Profile', width = 250, height = 250, command = lambda: print('Profile Page')).place(anchor = 'nw', relx = 0, rely = 0)

    if user.user_id[0] == 'S':
        ctk.CTkButton(login_frame, text = 'Booking History and Support', width = 250, height = 250, command = lambda: booking_history_support(user)).place(anchor = 'ne', relx = 1, rely = 0)
        ctk.CTkButton(login_frame, text = 'Approval Request and Outgoing Approvals', width = 250, height = 250, command = lambda: approval_request_page(user, card)).place(anchor = 'sw', relx = 0, rely = 1)
        ctk.CTkButton(login_frame, text = 'My Analytics', width = 250, height = 250, command = lambda: print('My Analytics Page')).place(anchor = 'se', relx = 1, rely = 1)
    else:
        ctk.CTkButton(login_frame, text = 'Response History', width = 250, height = 250, command = lambda: print('Response History')).place(anchor = 'ne', relx = 1, rely = 0)
        ctk.CTkButton(login_frame, text = 'Approval Management', width = 250, height = 250, command = lambda: approval_management_page(user, card)).place(anchor = 'sw', relx = 0, rely = 1)
        ctk.CTkButton(login_frame, text = 'School Analytics', width = 250, height = 250, command = lambda: print('Analytics Page')).place(anchor = 'se', relx = 1, rely = 1)

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
        timings_available_combobox.configure(state = 'active')
        timings_available_combobox.configure(values = timings_available)

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
    facility = ctk.StringVar()
    day = ctk.StringVar()
    timing = ctk.StringVar()
    
    #Frames
    main_frame = ctk.CTkFrame(window, width = 900, height = 600)
    main_frame.pack(expand = True, fill = 'both')
    outgoing_approval_frame = ctk.CTkFrame(window, borderwidth = 10, relief = ctk.CTkGROOVE)
    outgoing_approval_frame.pack(expand = True, fill = 'both')

    #Widgets
    ctk.CTkLabel(main_frame, text = 'Approval Request').pack()
    ctk.CTkLabel(main_frame, text = 'Request a new approval').pack()
    ctk.CTkLabel(main_frame, text = 'Pick Facility').pack()
    ctk.CTkCombobox(main_frame, textvariable = facility, values = facilities).pack()
    ctk.CTkLabel(main_frame, text = 'Pick Day').pack()
    ctk.CTkCombobox(main_frame, textvariable = day, values = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')).pack()
    ctk.CTkLabel(main_frame, text = 'Pick Timing').pack()
    timings_available_combobox = ctk.CTkCombobox(main_frame, state = 'disabled', textvariable = timing, values = [])
    timings_available_combobox.pack()
    ctk.CTkButton(main_frame, text = 'Check Available Timings', command = lambda: display_timings_available(day, facility, timings_available_combobox)).pack()
    ctk.CTkButton(main_frame, text = 'Request', command = lambda: user.request(day, facility, timing, timings_available_combobox)).pack()
    ctk.CTkButton(main_frame, text = 'Refresh', command = lambda: display_outgoing_approvals(user, outgoing_approval_frame)).pack()
    ctk.CTkButton(main_frame, text = '<--- HOME', command = lambda: home_page(user, card)).pack()
    #ctk.CTkButton(main_frame, text = 'Refresh', command = lambda: refresh_window(outgoing_approval_frame)).pack()
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
    main_frame = ctk.CTkFrame(window, width = 900, height = 600)
    main_frame.pack(expand = True, fill = 'both')
    incoming_approval_frame = ctk.CTkFrame(window, width = 900, height = 300, borderwidth = 10, relief = ctk.CTkGROOVE)
    incoming_approval_frame.pack(expand = True, fill = 'both')

    #Widgets
    ctk.CTkLabel(main_frame, text = 'Approval Request').pack()
    display_incoming_approvals(user, incoming_approval_frame, card)

def booking_history_support(user):

    def choose_or_other():
        if other_bool.get():
            text_box.configure(state = 'normal')
            problem_combobox.configure(state = 'disabled')
        else:
            text_box.configure(state = 'disabled')
            problem_combobox.configure(state = 'active')

    #Clear Page
    remove_widgets()

    #Variables
    problem = ctk.StringVar()
    facility = ctk.StringVar()
    other_bool = ctk.CTkBooleanVar()
    problems = ['Facility Damage', 'Facility Resources Empty', 'Theft of Facility Equipment', 'Health Hazard']
    facilities = ('Football', 'Sixth Form Room', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')


    #Frames
    main_frame = ctk.CTkFrame(window, width = 900, height = 600)
    main_frame.pack(expand = True, fill = 'both')
    selection_frame = ctk.CTkFrame(main_frame)

    #Grid
    selection_frame.rowconfigure(0, weight = 1)
    selection_frame.columnconfigure((0, 1), weight = 1)    

    #Widgets
    ctk.CTkLabel(main_frame, text = 'Request Problem').pack()
    ctk.CTkCombobox(main_frame, textvariable = facility, values = facilities).pack()
    selection_frame.pack()
    problem_radiobutton = ctk.CTkRadiobutton(selection_frame, value = False, variable = other_bool, command = lambda: choose_or_other())
    problem_radiobutton.grid(row = 0, column = 0)
    problem_combobox = ctk.CTkCombobox(selection_frame, textvariable = problem, values = problems)
    problem_combobox.grid(row = 0, column = 1)
    other_radiobutton = ctk.CTkRadiobutton(main_frame, text = 'Other', value = True, variable = other_bool, command = lambda: choose_or_other())
    other_radiobutton.pack()
    text_box = ctk.CTkText(main_frame, state = 'disabled')
    text_box.pack()
    submit_button = ctk.CTkButton(main_frame, text = 'Submit', command = lambda: user.request_problem(text_box, problem, problem_combobox, facility))
    submit_button.pack()

if __name__ == '__main__':
    login_page()
    window.mainloop()
