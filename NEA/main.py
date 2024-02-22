from tkinter import messagebox
from PIL import Image
from datetime import datetime, timedelta
import smtplib, hashlib, secrets, re, sqlite3, customtkinter as ctk      

conn = sqlite3.connect('rfid')
cursor = conn.cursor()

window = ctk.CTk(fg_color = '#ff7e75')
window.title('RFID System')
window.geometry('600x600')
window.resizable(False, False)
window_frame = ctk.CTkFrame(window, fg_color = '#ff7e75', corner_radius = 0, border_color = 'black', border_width = 2)
window_frame.pack(expand = True, fill = 'both')
ctk.set_appearance_mode('light')

class User: 
    def __init__(self, user_id, first_name, last_name, hashed_password, salt, grade, facility_id, login_count):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.hashed_password = hashed_password
        self.salt = salt
        self.grade = grade
        self.facility_id = facility_id
        self.login_count = login_count

class Card:
    def __init__(self, card_id = 0, tag_id = ''):
        self.card_id = card_id
        self.tag_id = tag_id

class Outgoing_Approval_Segment(ctk.CTkFrame):
    def __init__(self, parent, booking, status, outgoing_approvals):
        super().__init__(master = parent, border_color = "black", border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')
        self.booking = booking
        self.outgoing_approvals = outgoing_approvals
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1)
        close_button = ctk.CTkImage(light_image = Image.open("Images/close.png"), size = (22,22))
        ctk.CTkButton(self, text = self.booking[1], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 0)
        ctk.CTkButton(self, text = self.booking[2], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 1)
        ctk.CTkButton(self, text = self.booking[3], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 2)
        ctk.CTkButton(self, text = self.booking[4], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 3)
        ctk.CTkButton(self, text = self.booking[5], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 4)
        ctk.CTkButton(self, text = status, width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 5)
        ctk.CTkButton(self, text = '', image = close_button, width = 10, hover_color = '#d4d4d4', fg_color = '#F0F0F0', command = self.remove_booking,).grid(row = 0, column = 6)
    
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
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight = 1)
        close_button = ctk.CTkImage(light_image = Image.open("Images/close.png"), size = (22,22))
        check_button = ctk.CTkImage(light_image = Image.open("Images/check.png"), size = (22,22))
        ctk.CTkButton(self, text = self.booking[8], width = 50, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 0)
        ctk.CTkButton(self, text = self.booking[9], width = 50, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 1)
        ctk.CTkButton(self, text = self.booking[10], width = 50, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 2)
        ctk.CTkButton(self, text = self.booking[1], width = 50, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 3)
        ctk.CTkButton(self, text = self.booking[2], width = 50, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 4)
        ctk.CTkButton(self, text = self.booking[3], width = 50, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 5)
        ctk.CTkButton(self, text = self.booking[4], width = 50, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 6)
        ctk.CTkButton(self, text = self.booking[5], width = 50, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 7)
        ctk.CTkButton(self, text = '', image = check_button, width = 10, hover_color = '#d4d4d4', fg_color = '#F0F0F0', command = self.accept_booking).grid(row = 0, column = 8)
        ctk.CTkButton(self, text = '', image = close_button, width = 10, hover_color = '#d4d4d4', fg_color = '#F0F0F0', command = self.decline_booking).grid(row = 0, column = 9)

    def accept_booking(self):
        cursor.execute('UPDATE Timeslot SET status = TRUE WHERE timeslot_id = ?', (self.booking[7],))
        cursor.execute('UPDATE Booking SET approved = TRUE WHERE booking_number = ?', (self.booking[0],))
        conn.commit()
        self.delete_approval_object()

    def decline_booking(self):
        cursor.execute('UPDATE Timeslot SET status = FALSE WHERE timeslot_id = ?', (self.card.card_id,))
        cursor.execute('UPDATE Booking SET approved = FALSE WHERE booking_number = ?', (self.booking[0]))
        conn.commit()
        self.delete_approval_object()

    def delete_approval_object(self):
        for approval in self.incoming_approvals: 
            if approval.booking[0] == self.booking[0]:
                for widget in approval.winfo_children():
                    widget.destroy()
                self.incoming_approvals.remove(approval)
                del approval   

class ContentFrame(ctk.CTkFrame):
    def __init__(self, parent, user, card):
        super().__init__(parent, width = 650, height = 550, border_color = "black", border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')
        self.user = user
        self.card = card
        ctk.CTkLabel(self, text = 'Welcome!', font = ('Impact', 140)).place(anchor = 'center', relx = 0.5, rely = 0.5)

#Facility Support
    def facility_support(self):
        self.clear_frame()
        #Variables
        self.problem = ctk.StringVar()
        self.facility = ctk.StringVar()
        self.other_bool = ctk.BooleanVar()
        self.problems = ['Facility Damage', 'Facility Resources Empty', 'Theft of Facility Equipment', 'Health Hazard']
        self.facilities = ('Football', 'Sixth Form Room', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')

        #Widgets
        ctk.CTkLabel(self, text = 'Facility Support', font = ('Impact', 90)).place(anchor = 'center', relx = 0.5, rely = 0.15)
        ctk.CTkLabel(self, text = 'Choose Facility', font = ('Impact', 40)).place(anchor = 'center', relx = 0.3, rely = 0.35)
        ctk.CTkComboBox(self, state = 'readonly', border_color = 'black', button_color = 'black', variable = self.facility, values = self.facilities, width = 250, dropdown_font = ('Impact', 15)).place(anchor = 'center', relx = 0.7, rely = 0.35)
        ctk.CTkLabel(self, text = 'Choose Problem', font = ('Impact', 37)).place(anchor = 'center', relx = 0.3, rely = 0.5)
        self.problem_combobox = ctk.CTkComboBox(self, state = 'readonly', border_color = 'black', button_color = 'black', width = 250, dropdown_font = ('Impact', 15), variable = self.problem, values = self.problems)
        self.problem_combobox.place(anchor = 'center', relx = 0.7, rely = 0.5)
        self.other_button = ctk.CTkSwitch(self, text = 'Other', command = self.other, variable = self.other_bool, progress_color = '#ff7e75', button_color = 'black')
        self.other_button.place(anchor = 'center', relx = 0.5, rely = 0.6)
        self.other_texbox = ctk.CTkTextbox(self, state = 'disabled', width = 400, height = 100, border_color = 'black', border_width = 2)
        self.other_texbox.place(anchor = 'n', relx = 0.5, rely = 0.65)
        self.submit_button = ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', text = 'Submit', font = ('Impact', 20), command = self.request_problem)
        self.submit_button.place(anchor = 'center', relx = 0.5, rely = 0.9)

    def other(self):
        if self.other_bool.get() == True:
            self.other_texbox.configure(state = 'normal')
            self.problem_combobox.configure(state = 'disabled')
        else:
            self.other_texbox.configure(state = 'disabled')
            self.problem_combobox.configure(state = 'readonly')

    def request_problem(self):
        other_problem = self.other_texbox.get(1.0, "end-1c")
        if self.facility.get() != '' or other_problem != '':
            facility_id_db = cursor.execute('SELECT facility_id FROM Facility WHERE facility_name = ?;', (self.facility.get(),)).fetchall()
            if self.other_bool.get() == False:
                issue_id_db = cursor.execute('SELECT issue_id FROM Issue WHERE issue = ?;', (self.problem.get(),)).fetchall()
                cursor.execute('INSERT INTO IssueRequest (issue_id, facility_id, resolved) VALUES (?, ?, FALSE);', (issue_id_db[0][0], facility_id_db[0][0]))
                conn.commit()
                
            else:
                cursor.execute('INSERT INTO IssueRequest (issue_id, facility_id, other_issue_reason, resolved) VALUES (0, ?, ?, FALSE);', (facility_id_db[0][0], other_problem))
                conn.commit()
            messagebox.showinfo('Request Successful', 'Your issue will be fixed.')
        else:
            messagebox.showerror("Request Failed", "All fields must be filled out.")

#Approval Request
    def approval_request(self):
        self.clear_frame()
        #Variables
        self.facilities = ('Football', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')
        self.days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
        self.facility = ctk.StringVar()
        self.day = ctk.StringVar()
        self.timing = ctk.StringVar()

        #Widgets
        ctk.CTkLabel(self, text = 'Approval Request', font = ('Impact', 85)).place(anchor = 'center', relx = 0.5, rely = 0.15)
        ctk.CTkLabel(self, text = 'Choose Facility', font = ('Impact', 40)).place(anchor = 'center', relx = 0.3, rely = 0.35)
        ctk.CTkLabel(self, text = 'Pick Day', font = ('Impact', 40)).place(anchor = 'center', relx = 0.3, rely = 0.5)
        ctk.CTkLabel(self, text = 'Pick Timing', font = ('Impact', 40)).place(anchor = 'center', relx = 0.3, rely = 0.65)
        ctk.CTkComboBox(self, state = 'readonly', border_color = 'black', button_color = 'black', width = 250, dropdown_font = ('Impact', 15), variable = self.facility, values = self.facilities).place(anchor = 'center', relx = 0.7, rely = 0.35)
        ctk.CTkComboBox(self, state = 'readonly', border_color = 'black', button_color = 'black', width = 250, dropdown_font = ('Impact', 15), variable = self.day, values = self.days, command = self.display_timings_available).place(anchor = 'center', relx = 0.7, rely = 0.5)
        self.timings_available_combobox = ctk.CTkComboBox(self, state = 'disabled', border_color = 'black', button_color = 'black', width = 250, dropdown_font = ('Impact', 15), variable = self.timing, values = [])
        self.timings_available_combobox.place(anchor = 'center', relx = 0.7, rely = 0.65)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', text = 'Request', font = ('Impact', 20), command = self.request).place(anchor = 'center', relx = 0.5, rely = 0.8)        

    def display_timings_available(self, event):
        timings_available = []
        timings = cursor.execute('''SELECT Timeslot.start_time, Timeslot.end_time 
                                FROM Timeslot 
                                JOIN Facility ON Facility.facility_id = Timeslot.facility_id 
                                WHERE Timeslot.day = ? 
                                    AND Facility.facility_name = ? 
                                    AND Timeslot.status = 0;''' ,(self.day.get(), self.facility.get())).fetchall()
        for slot in timings:
            timings_available.append(f'{slot[0][:-3]} - {slot[1][:-3]}')
        self.timings_available_combobox.configure(state = 'readonly')
        self.timings_available_combobox.configure(values = timings_available)

    def get_time(self):
        timing_format = self.timing.get()
        for index in range(len(timing_format)):
            if timing_format[index] == '-':
                self.start_time = f'{timing_format[:index - 1].strip()}:00'
                self.end_time = f'{timing_format[index + 1:].strip()}:00'
        day = self.day.get()
        today = datetime.today()
        Day_num = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4}
        days_delta = (Day_num[day] - today.weekday()) % 7
        self.date = (today + timedelta(days=days_delta)).strftime('%Y-%m-%d')

    def request(self):
        self.get_time()
        facility_id_db = cursor.execute('SELECT facility_id FROM Facility WHERE facility_name = ?', (self.facility.get(), )).fetchall()
        self.timeslot_id_db = cursor.execute('SELECT timeslot_id FROM Timeslot WHERE day = ? AND facility_id = ? AND start_time = ? AND end_time = ?', (self.day.get(), facility_id_db[0][0], self.start_time, self.end_time)).fetchall()
        cursor.execute('INSERT INTO Booking (facility_id, user_id, timeslot_id, booking_date) VALUES (?, ?, ?, ?)', (facility_id_db[0][0], self.user.user_id, self.timeslot_id_db[0][0], self.date))
        cursor.execute('UPDATE Timeslot SET status = NULL WHERE timeslot_id = ?', (self.timeslot_id_db[0][0],))
        conn.commit()
        self.timing.set('')
        self.timings_available_combobox.configure(state = 'disabled')
        messagebox.showinfo('Request Successful', f'Requested {self.facility.get()} from {self.start_time} to {self.end_time} on {self.day.get()} {self.date}')

#Card Tap in
    def card_tap_in_page(self):
        self.clear_frame()
        self.facility_choice = ctk.StringVar()
        self.facilities = ('Football', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')
        ctk.CTkComboBox(self, values = self.facilities, variable = self.facility_choice).place(anchor = 'center', relx = 0.5, rely = 0.2)
        ctk.CTkButton(self, text = 'Tap In', command = self.card_tap_in_func).place(anchor = 'center', relx = 0.5, rely = 0.4) 

    def card_tap_in_func(self):
        current_date_time = datetime.now()
        self.current_time = current_date_time.strftime('%H:%M:%S')
        self.current_date = current_date_time.strftime('%Y-%m-%d')
        self.facility_booking_required = cursor.execute('''SELECT facility_id, booking_required 
                                                FROM Facility
                                                WHERE facility_name = ?''', (self.facility_choice.get(),)).fetchall()
        if self.user.user_id[0] == 'A':
            self.access_granted()
        elif self.user.user_id[0] == 'T':
            if self.user.facility_id == self.facility_booking_required[0][0] or self.facility_booking_required[0][1] == 0:
                self.access_granted()
            else:
                self.access_denied()
        elif self.user.user_id[0] == 'S':    
            if self.facility_booking_required[0][1] == 1:
                booking_date_info = cursor.execute('''SELECT start_time, end_time, booking_date
                                                    FROM User, Booking, Timeslot
                                                    WHERE User.user_id = Booking.user_id
                                                    AND User.user_id = ?
                                                    AND Booking.facility_id = ?
                                                    AND Timeslot.timeslot_id = Booking.timeslot_id
                                                    AND Timeslot.status = 1
                                                    AND Timeslot.start_time <= ?
                                                    AND Timeslot.end_time >= ?
                                                    AND Booking.booking_date = ?''', 
                                                    (self.user.user_id, self.facility_booking_required[0][0], self.current_time, self.current_time, self.current_date)).fetchall()
                if booking_date_info != []:
                    self.access_granted()
                else:
                    self.access_denied()
            elif self.facility_booking_required[0][1] == 0:
                self.access_granted()
        conn.commit()

    def access_granted(self):
        cursor.execute('''INSERT INTO Swipe (card_id, facility_id, date, time, access_accepted)
                                        VALUES (?, ?, ?, ?, TRUE)''',
                                        (self.card.card_id, self.facility_booking_required[0][0], self.current_date, self.current_time))
        messagebox.showinfo('', 'Access Granted')

    def access_denied(self):
        cursor.execute('''INSERT INTO Swipe (card_id, facility_id, date, time, access_accepted)
                        VALUES (?, ?, ?, ?, FALSE)''',
                        (self.card.card_id, self.facility_booking_required[0][0], self.current_date, self.current_time))
        messagebox.showerror('', 'Access Denied')

#Outgoing Student Approvals
    def outgoing_approvals(self):
        self.clear_frame()
        bookings = cursor.execute('''SELECT Booking.booking_number, Facility.facility_name, Timeslot.start_time, Timeslot.end_time, Timeslot.day, Booking.booking_date, Booking.approved, Booking.timeslot_id 
                                    FROM Facility, Timeslot, Booking 
                                    WHERE Facility.facility_id = Booking.facility_id
                                        AND Timeslot.timeslot_id = Booking.timeslot_id
                                        AND Booking.user_id = ?;''', (self.user.user_id,)).fetchall()
        if bookings != []:
            outgoing_approvals = []
            for booking in bookings:
                if booking[6] == None: status = 'Pending'
                elif booking[6] == 1: status = 'Approved'
                else: status = 'Declined'
                approval = Outgoing_Approval_Segment(self, booking, status, outgoing_approvals)
                outgoing_approvals.append(approval)
            title_font = ctk.CTkFont(family = 'Impact', size = 18, underline = True)
            ctk.CTkLabel(self, text = 'Sent Approvals', font = ('Impact', 90)).place(anchor = 'center', relx = 0.5, rely = 0.15)
            ctk.CTkLabel(self, text = 'Facility', font = title_font).place(anchor = 'center', relx = 0.085, rely = 0.33)
            ctk.CTkLabel(self, text = 'Start Time', font = title_font).place(anchor = 'center', relx = 0.24, rely = 0.33)
            ctk.CTkLabel(self, text = 'End Time', font = title_font).place(anchor = 'center', relx = 0.39, rely = 0.33)
            ctk.CTkLabel(self, text = 'Day', font = title_font).place(anchor = 'center', relx = 0.545, rely = 0.33)
            ctk.CTkLabel(self, text = 'Date', font = title_font).place(anchor = 'center', relx = 0.695, rely = 0.33)
            ctk.CTkLabel(self, text = 'Status', font = title_font).place(anchor = 'center', relx = 0.855, rely = 0.33)
            for request in range(len(outgoing_approvals)):
                outgoing_approvals[request].place(anchor = 'center', relx = 0.5, rely = (request / 10) + 0.4)
        else:
            ctk.CTkLabel(self, text = 'You have no requests sent', font = ('Impact', 50)).place(anchor = 'center', relx = 0.5, rely = 0.5)

#Incoming Admin Approvals
    def all_approvals(self):
        self.clear_frame()
        bookings = cursor.execute('''SELECT Booking.booking_number, Facility.facility_name, Timeslot.start_time, Timeslot.end_time, Timeslot.day, Booking.booking_date, Booking.approved, Booking.timeslot_id, User.first_name, User.last_name, User.class_grade, User.user_id
                                    FROM Facility, Timeslot, Booking, User
                                    WHERE Booking.facility_id = Facility.facility_id
                                    AND Booking.approved IS NULL
                                    AND Booking.timeslot_id = Timeslot.timeslot_id
                                    AND User.user_id = Booking.user_id;''').fetchall()
        if bookings != []:
            incoming_approvals = []
            for booking in bookings:
                approval = Incoming_Approval_Segment(self, incoming_approvals, booking, self.card)
                incoming_approvals.append(approval)
            title_font = ctk.CTkFont(family = 'Impact', size = 18, underline = True)
            ctk.CTkLabel(self, text = 'Sent Approvals', font = ('Impact', 90)).place(anchor = 'center', relx = 0.5, rely = 0.15)
            ctk.CTkLabel(self, text = 'Facility', font = title_font).place(anchor = 'center', relx = 0.085, rely = 0.33)
            ctk.CTkLabel(self, text = 'Start Time', font = title_font).place(anchor = 'center', relx = 0.24, rely = 0.33)
            ctk.CTkLabel(self, text = 'End Time', font = title_font).place(anchor = 'center', relx = 0.39, rely = 0.33)
            ctk.CTkLabel(self, text = 'Day', font = title_font).place(anchor = 'center', relx = 0.545, rely = 0.33)
            ctk.CTkLabel(self, text = 'Date', font = title_font).place(anchor = 'center', relx = 0.695, rely = 0.33)
            ctk.CTkLabel(self, text = 'Status', font = title_font).place(anchor = 'center', relx = 0.855, rely = 0.33)
            for request in range(len(incoming_approvals)):
                incoming_approvals[request].place(anchor = 'center', relx = 0.5, rely = (request / 10) + 0.4)
        else:
            ctk.CTkLabel(self, text = 'You have no requests sent', font = ('Impact', 50)).place(anchor = 'center', relx = 0.5, rely = 0.5)        

#Incoming Teacher Approvals
    def incoming_teacher_approvals(self):
        self.clear_frame()
        bookings = cursor.execute('''SELECT Booking.booking_number, Facility.facility_name, Timeslot.start_time, Timeslot.end_time, Timeslot.day, Booking.booking_date, Booking.approved, Booking.timeslot_id, User.first_name, User.last_name, User.class_grade, User.user_id
                                    FROM Facility, Timeslot, Booking, User
                                    WHERE Booking.facility_id = Facility.facility_id
                                    AND Booking.approved IS NULL
                                    AND Booking.facility_id = ?
                                    AND Booking.timeslot_id = Timeslot.timeslot_id
                                    AND User.user_id = Booking.user_id;''', (self.user.facility,)).fetchall()
        if bookings != []:
            incoming_approvals = []
            for booking in bookings:
                approval = Incoming_Approval_Segment(self, incoming_approvals, booking, self.card)
                incoming_approvals.append(approval)
            title_font = ctk.CTkFont(family = 'Impact', size = 18, underline = True)
            ctk.CTkLabel(self, text = 'Sent Approvals', font = ('Impact', 90)).place(anchor = 'center', relx = 0.5, rely = 0.15)
            ctk.CTkLabel(self, text = 'Facility', font = title_font).place(anchor = 'center', relx = 0.085, rely = 0.33)
            ctk.CTkLabel(self, text = 'Start Time', font = title_font).place(anchor = 'center', relx = 0.24, rely = 0.33)
            ctk.CTkLabel(self, text = 'End Time', font = title_font).place(anchor = 'center', relx = 0.39, rely = 0.33)
            ctk.CTkLabel(self, text = 'Day', font = title_font).place(anchor = 'center', relx = 0.545, rely = 0.33)
            ctk.CTkLabel(self, text = 'Date', font = title_font).place(anchor = 'center', relx = 0.695, rely = 0.33)
            ctk.CTkLabel(self, text = 'Status', font = title_font).place(anchor = 'center', relx = 0.855, rely = 0.33)
            for request in range(len(incoming_approvals)):
                    incoming_approvals[request].place(anchor = 'center', relx = 0.5, rely = (request / 10) + 0.4)
        else:
            ctk.CTkLabel(self, text = 'You have no requests sent', font = ('Impact', 50)).place(anchor = 'center', relx = 0.5, rely = 0.5)

#Reset Content Frame
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

class SideBar(ctk.CTkFrame):
    def __init__(self, parent, login, page):
        super().__init__(parent, width = 200, height = 600, border_color = "black", border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')
        profile_icon = ctk.CTkImage(light_image = Image.open("Images/profile.png"), size = (70,70))
        if login.user.user_id[0] == 'A':
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = '', image = profile_icon, width = 100, height = 100, text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.15)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Approvals', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.all_approvals).place(anchor = 'center', relx = 0.5, rely = 0.35)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Tap In', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.card_tap_in_page).place(anchor = 'center', relx = 0.5, rely = 0.45)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Schedule', text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.55)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Analytics', text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.63)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Response History', text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.75)
        elif login.user.user_id[0] == 'T':
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = '', image = profile_icon, width = 100, height = 100, text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.15)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Approvals', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.incoming_teacher_approvals).place(anchor = 'center', relx = 0.5, rely = 0.35)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Tap In', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.card_tap_in_page).place(anchor = 'center', relx = 0.5, rely = 0.45)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Schedule', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.approval_request).place(anchor = 'center', relx = 0.5, rely = 0.55)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Analytics', text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.63)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Response History', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.facility_support).place(anchor = 'center', relx = 0.5, rely = 0.75)
        elif login.user.user_id[0] == 'S':
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = '', image = profile_icon, width = 100, height = 100, text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.15)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Facility Support', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.facility_support).place(anchor = 'center', relx = 0.5, rely = 0.35)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Tap In', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.card_tap_in_page).place(anchor = 'center', relx = 0.5, rely = 0.45)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Approval Request', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.approval_request).place(anchor = 'center', relx = 0.5, rely = 0.55)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'View Sent Approvals', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.outgoing_approvals).place(anchor = 'center', relx = 0.5, rely = 0.63)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Approval Request History', text_color = 'black', fg_color = 'white', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.75)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Logout', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = login.logout_func).place(anchor = 'center', relx = 0.5, rely = 0.93)

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, user = None, card = None):
        #Page Initialisation
        super().__init__(parent, width = 200, height = 600, border_color = "black", border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')
        window.geometry('600x600')
        remove_widgets_login_register()
        #Variables
        self.id_entry = ctk.StringVar()
        self.password_entry = ctk.StringVar()
        self.user = user
        self.card = card
        password_icon = ctk.CTkImage(light_image = Image.open("Images/padlock.png"), size = (22,22))
        id_icon = ctk.CTkImage(light_image = Image.open("Images/id.png"), size = (22,22))
        
        #Frames
        login_frame = ctk.CTkFrame(window_frame, width = 500, height = 500, border_color = 'black', border_width = 2, fg_color = '#F0F0F0', corner_radius = 0)
        login_frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

        #Widgets
        ctk.CTkLabel(login_frame, text = 'User Login', font = ('Impact', 70)).place(anchor = 'center', relx = 0.5, rely = 0.25)
        ctk.CTkLabel(login_frame, text = '', image = id_icon).place(anchor = 'center', relx = 0.33, rely = 0.4)
        ctk.CTkLabel(login_frame, text = 'User ID', font = ('Impact', 20)).place(anchor = 'center', relx = 0.42, rely = 0.4)
        ctk.CTkEntry(login_frame, textvariable = self.id_entry, width = 200, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.5, rely = 0.45)
        ctk.CTkLabel(login_frame, text = '', image = password_icon).place(anchor = 'center', relx = 0.33, rely = 0.525)
        ctk.CTkLabel(login_frame, text = 'Password', font = ('Impact', 20)).place(anchor = 'center', relx = 0.44, rely = 0.53)
        ctk.CTkEntry(login_frame, textvariable = self.password_entry, show = '*', width = 200, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.5, rely = 0.58)
        ctk.CTkButton(login_frame, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = 'Login', text_color = 'black', fg_color = 'white', font = ('Impact', 25), command = self.login_func).place(anchor = 'center', relx = 0.5, rely = 0.7)
        ctk.CTkLabel(login_frame, text = 'or').place(anchor = 'center', relx = 0.5, rely = 0.77)
        ctk.CTkButton(login_frame, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Don't have an account? Register Here", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = lambda: RegisterPage(window_frame)).place(anchor = 'center', relx = 0.5, rely = 0.84)

    def login_func(self):
        self.user_db = cursor.execute('''SELECT * 
                                      FROM User 
                                      WHERE user_id = ?;''', 
                                      (self.id_entry.get(),)).fetchall()
        if self.user_db[0][4] == None:
            messagebox.showerror('Login Failed', 'Please set a new password.')
        elif self.password_check():
            self.card_db = cursor.execute('''SELECT card_id, tag_id 
                                       FROM Card 
                                       WHERE user_id = ?;''', 
                                       (self.user_db[0][0],)).fetchall()
            self.card, self.user = Card(self.card_db[0][0], self.card_db[0][1]), User(self.user_db[0][0], self.user_db[0][2], self.user_db[0][3], self.user_db[0][4], self.user_db[0][5], self.user_db[0][6], self.user_db[0][1], self.user_db[0][7])
            messagebox.showinfo('Login Successful', f'Welcome, {self.user_db[0][2]} {self.user_db[0][3]}')
            main(self)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def password_check(self):
        salted_password = self.password_entry.get().encode('utf-8') + self.user_db[0][5]
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        if hashed_password == self.user_db[0][4]: return True
        else: return False

    def logout_func(self):
        messagebox.showinfo('Logout Successful', f'Goodbye, {self.user_db[0][2]} {self.user_db[0][3]}')
        remove_widgets_login_register()
        del self
        main(login = None)

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width = 200, height = 600, border_color = "black", border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')    
        remove_widgets_login_register()
        #Variables
        self.id_entry = ctk.StringVar()
        self.password_entry = ctk.StringVar()
        self.confirm_password_entry = ctk.StringVar()

        #Frames
        login_frame = ctk.CTkFrame(window_frame, width = 500, height = 500, border_color = "black", fg_color = '#F0F0F0', border_width = 2, corner_radius = 0)
        login_frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

        #Widgets
        ctk.CTkLabel(login_frame, text = 'Set New Password', font = ('Impact', 70)).place(anchor = 'center', relx = 0.5, rely = 0.17)
        ctk.CTkLabel(login_frame, text = 'User ID', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.25)
        ctk.CTkEntry(login_frame, textvariable = self.id_entry, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.5, rely = 0.3)
        ctk.CTkLabel(login_frame, text = 'Password', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.4)
        ctk.CTkEntry(login_frame, textvariable = self.password_entry, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.5, rely = 0.45)
        ctk.CTkLabel(login_frame, text = 'Confirm Password', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.55)
        ctk.CTkEntry(login_frame, textvariable = self.confirm_password_entry, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.5, rely = 0.6)

        ctk.CTkButton(login_frame, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Set", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.register_new_password_func).place(anchor = 'center', relx = 0.5, rely = 0.79)
        ctk.CTkLabel(login_frame, text = 'or').place(anchor = 'center', relx = 0.5, rely = 0.86)
        ctk.CTkButton(login_frame, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Go to Login", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = lambda: LoginPage(window_frame)).place(anchor = 'center', relx = 0.5, rely = 0.93)

    def register_new_password_func(self):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        login_count = cursor.execute('''SELECT login_count 
                                    FROM User 
                                    WHERE user_id = ?;''', 
                                    (self.id_entry.get(),)).fetchall()
        if login_count[0][0] == 0:
            if self.id_entry.get() == '' or self.password_entry.get() == '' or self.confirm_password_entry.get() == '':
                messagebox.showerror("Register Failed", "All fields must be filled out.")
            elif self.password_entry.get() != self.confirm_password_entry.get():
                messagebox.showerror("Register Failed", "Please make sure the passwords are the same.")
            elif not re.match(pattern, self.password_entry.get()):
                messagebox.showerror("Register Failed", "Password is not strong enough. Please include: 8 Characters minimum, A capital letter, A small letter, A number, A symbol.")
            elif re.match(pattern, self.password_entry.get()):
                hashed_password, salt = self.password_hash()
                card = cursor.execute('SELECT card_id FROM Card WHERE user_id IS NULL LIMIT 1;').fetchall()
                cursor.execute('''UPDATE Card 
                               SET user_id = ? 
                               WHERE card_id = ?;''', 
                               (self.id_entry.get(), card[0][0]))
                cursor.execute('''UPDATE User 
                               SET hashed_password = ?, salt = ?
                               WHERE user_id = ?;''', 
                               (hashed_password, salt, self.id_entry.get()))
                messagebox.showinfo('Password Successfully Set', 'Please login with the new password.')
                conn.commit()
                LoginPage(window_frame)
        else:
            messagebox.showerror("Password Set Failed", "Accounts password has already been changed please change from user settings.")
    
    def password_hash(self):
        salt = secrets.token_bytes(16)
        salted_password = self.password_entry.get().encode('utf-8') + salt
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        return hashed_password, salt

def remove_widgets_login_register():
    #Removes every widget on the page by cyclying through them and destroying them
    for widget in window_frame.winfo_children():
        widget.destroy()

def email(subject, body):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('3465@ascsdubai.ae', 'Mario@School24')
        smtp.sendmail('3465@ascsdubai.ae', 'skatedany26@gmail.com', f'Subject: {subject}\n\n{body}')

def main(login = None):
    if login != None:
        remove_widgets_login_register()
        window.geometry('900x600')
        page = ContentFrame(window_frame, login.user, login.card)
        sidebar = SideBar(window_frame, login, page)
        sidebar.place(anchor = 'nw', relx = 0, rely = 0)
        page.place(anchor = 'center', relx = 0.61, rely = 0.5)
    else:
        login = LoginPage(window_frame)

if __name__ == '__main__':
    main(login = None)
    window.mainloop()
