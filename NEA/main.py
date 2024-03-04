from tkinter import messagebox
from PIL import Image
from datetime import datetime, timedelta
from ttkbootstrap.dialogs import Querybox
import smtplib, hashlib, secrets, re, sqlite3, mplcursors, customtkinter as ctk, matplotlib.pyplot as plt, matplotlib.dates as mdates

conn = sqlite3.connect('rfid')
cursor = conn.cursor()

theme_color = '#ff7e75'
window = ctk.CTk(fg_color = theme_color)
window.title('RFID System')
window.geometry('600x600')
window.resizable(False, False)
window_frame = ctk.CTkFrame(window, fg_color = theme_color, corner_radius = 0, border_color = 'black', border_width = 2)
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
    def __init__(self, card_id, tag_id):
        self.card_id = card_id
        self.tag_id = tag_id

class Outgoing_Approval_Segment(ctk.CTkFrame):
    def __init__(self, parent, booking, status, outgoing_approval_objects):
        super().__init__(master = parent, border_color = "black", border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')
        self.booking = booking
        self.outgoing_approval_objects = outgoing_approval_objects
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1)
        ctk.CTkButton(self, text = self.booking[1], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 0)
        ctk.CTkButton(self, text = self.booking[2], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 1)
        ctk.CTkButton(self, text = self.booking[3], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 2)
        ctk.CTkButton(self, text = self.booking[4], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 3)
        ctk.CTkButton(self, text = self.booking[5], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 4)
        ctk.CTkButton(self, text = status, width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 5)
        if status != 'Approved':
            close_button = ctk.CTkImage(light_image = Image.open("Images/close.png"), size = (22,22))
            ctk.CTkButton(self, text = '', image = close_button, width = 10, hover_color = '#F0F0F0', fg_color = '#d4d4d4', bg_color = '#d4d4d4', command = self.remove_booking,).grid(row = 0, column = 6)
        self.pack(pady = 10)

    def remove_booking(self):
        cursor.execute('UPDATE Timeslot SET status = FALSE WHERE timeslot_id = ?', (self.booking[7],))
        cursor.execute('DELETE FROM Booking WHERE booking_number = ?', (self.booking[0],))
        conn.commit()
        for approval_object in self.outgoing_approval_objects: 
            if approval_object.booking[0] == self.booking[0]:
                for widget in approval_object.winfo_children():
                    widget.destroy()
                self.outgoing_approval_objects.remove(approval_object)
                del approval_object

class Incoming_Approval_Segment(ctk.CTkFrame):
    def __init__(self, parent, incoming_approval_objects, booking, card):
        super().__init__(master = parent)
        self.card = card
        self.incoming_approval_objects = incoming_approval_objects
        self.booking = booking
        self.toplevel_window = None
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight = 1)
        close_button = ctk.CTkImage(light_image = Image.open("Images/close.png"), size = (22,22))
        check_button = ctk.CTkImage(light_image = Image.open("Images/check.png"), size = (22,22))
        ctk.CTkButton(self, text = self.booking[11], width = 80, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover_color = '#d4d4d4', corner_radius = 0, command = self.open_toplevel).grid(row = 0, column = 0)
        ctk.CTkButton(self, text = self.booking[1], width = 80, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 1)
        ctk.CTkButton(self, text = self.booking[2], width = 80, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 2)
        ctk.CTkButton(self, text = self.booking[3], width = 80, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 3)
        ctk.CTkButton(self, text = self.booking[4], width = 80, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 4)
        ctk.CTkButton(self, text = self.booking[5], width = 80, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 5)
        ctk.CTkButton(self, text = '', image = check_button, width = 10, hover_color = '#F0F0F0', fg_color = '#d4d4d4', bg_color = '#d4d4d4', command = self.accept_booking).grid(row = 0, column = 8)
        ctk.CTkButton(self, text = '', image = close_button, width = 10, hover_color = '#F0F0F0', fg_color = '#d4d4d4', bg_color = '#d4d4d4', command = self.decline_booking).grid(row = 0, column = 9)
        self.pack(pady = 10)

    def accept_booking(self):
        cursor.execute('UPDATE Timeslot SET status = TRUE WHERE timeslot_id = ?', (self.booking[7],))
        cursor.execute('UPDATE Booking SET approved = TRUE WHERE booking_number = ?', (self.booking[0],))
        conn.commit()
        self.delete_approval_object()

    def decline_booking(self):
        cursor.execute('UPDATE Timeslot SET status = FALSE WHERE timeslot_id = ?', (self.card.card_id,))
        cursor.execute('UPDATE Booking SET approved = FALSE WHERE booking_number = ?', (self.booking[0],))
        conn.commit()
        self.delete_approval_object()

    def delete_approval_object(self):
        for approval_object in self.incoming_approval_objects: 
            if approval_object.booking[0] == self.booking[0]:
                for widget in approval_object.winfo_children():
                    widget.destroy()
                self.incoming_approval_objects.remove(approval_object)
                del approval_object 

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = StudentProfile(self.booking, self.card)
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

class Scheduled_Booking_Segment(ctk.CTkFrame):
    def __init__(self, parent, booking_objects, booking, card, user):
        super().__init__(master = parent)
        self.booking_objects = booking_objects
        self.user = user
        self.card = card
        self.booking = booking
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1)
        ctk.CTkButton(self, text = self.booking[11], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover_color = '#d4d4d4', corner_radius = 0, command = self.open_toplevel).grid(row = 0, column = 0)
        ctk.CTkButton(self, text = self.booking[1], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 1)
        ctk.CTkButton(self, text = self.booking[2], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 2)
        ctk.CTkButton(self, text = self.booking[3], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 3)
        ctk.CTkButton(self, text = self.booking[4], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 4)
        ctk.CTkButton(self, text = self.booking[5], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 5)
        self.toplevel_window = None
        if self.user.user_id[0] == 'A':
            close_button = ctk.CTkImage(light_image = Image.open("Images/close.png"), size = (22,22))
            ctk.CTkButton(self, text = '', image = close_button, width = 10, hover_color = '#F0F0F0', fg_color = '#d4d4d4', bg_color = '#d4d4d4', command = self.decline_booking).grid(row = 0, column = 6)
        self.pack(pady = 10)
    
    def decline_booking(self):
        cursor.execute('UPDATE Timeslot SET status = FALSE WHERE timeslot_id = ?', (self.card.card_id,))
        cursor.execute('UPDATE Booking SET approved = FALSE WHERE booking_number = ?', (self.booking[0],))
        conn.commit()
        for booking_object in self.booking_objects: 
            if booking_object.booking[0] == self.booking[0]:
                for widget in booking_object.winfo_children():
                    widget.destroy()
                self.booking_objects.remove(booking_object)
                del booking_object 
  
    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = StudentProfile(self.booking, self.card)
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

class StudentProfile(ctk.CTkToplevel):
    def __init__(self, booking, card, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x300")
        self.title('Student Info')

        window_frame = ctk.CTkFrame(self, width = 300, height = 300, border_color = 'black', border_width = 2, fg_color = theme_color, corner_radius = 0)
        window_frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

        info_frame = ctk.CTkFrame(self, width = 250, height = 250, border_color = 'black', border_width = 2, fg_color = '#F0F0F0', corner_radius = 0)
        info_frame.place(anchor = 'center', relx = 0.5, rely = 0.5)
        info_frame.rowconfigure(0, weight = 1)
        info_frame.columnconfigure((0, 1, 2, 3, 4), weight = 1)

        title_font = ctk.CTkFont(family = 'Impact', size = 18, underline = True)
        info_font = ctk.CTkFont(family = 'Impact', size = 18)
        ctk.CTkLabel(info_frame, text = 'User ID:', font = title_font).place(anchor = 'e', relx = 0.5, rely = 0.1)
        ctk.CTkLabel(info_frame, text = 'Card ID:', font = title_font).place(anchor = 'e', relx = 0.5, rely = 0.3)
        ctk.CTkLabel(info_frame, text = 'First Name:', font = title_font).place(anchor = 'e', relx = 0.5, rely = 0.5)
        ctk.CTkLabel(info_frame, text = 'Last Name:', font = title_font).place(anchor = 'e', relx = 0.5, rely = 0.7)
        ctk.CTkLabel(info_frame, text = 'Class:', font = title_font).place(anchor = 'e', relx = 0.5, rely = 0.9)
        ctk.CTkLabel(info_frame, text = booking[11], font = info_font).place(anchor = 'w', relx = 0.53, rely = 0.1)
        ctk.CTkLabel(info_frame, text = card.card_id, font = info_font).place(anchor = 'w', relx = 0.53, rely = 0.3)
        ctk.CTkLabel(info_frame, text = booking[8], font = info_font).place(anchor = 'w', relx = 0.53, rely = 0.5)
        ctk.CTkLabel(info_frame, text = booking[9], font = info_font).place(anchor = 'w', relx = 0.53, rely = 0.7)
        ctk.CTkLabel(info_frame, text = booking[10], font = info_font).place(anchor = 'w', relx = 0.53, rely = 0.9)

class Records(ctk.CTkFrame):
    def __init__(self, parent, user, record, records):
        super().__init__(master = parent, border_color = "black", border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')
        self.records = records
        self.user = user
        self.record = record
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight = 1)
        ctk.CTkButton(self, text = self.record[0], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 0)
        ctk.CTkButton(self, text = self.record[1], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 1)
        ctk.CTkButton(self, text = self.record[2], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 2)
        ctk.CTkButton(self, text = self.record[3], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 3)
        ctk.CTkButton(self, text = self.record[4], width = 100, border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 18), hover = False, corner_radius = 0).grid(row = 0, column = 4)
        if self.user.user_id[0] == 'A':
            close_button = ctk.CTkImage(light_image = Image.open("Images/close.png"), size = (22,22))
            ctk.CTkButton(self, text = '', image = close_button, width = 10, hover_color = '#F0F0F0', fg_color = '#d4d4d4', bg_color = '#d4d4d4', command = self.remove_record).grid(row = 0, column = 8)
        self.pack(pady = 10)
    
    def remove_record(self):
        cursor.execute('UPDATE CARD SET user_id = NULL WHERE user_id = ?', (self.record[0],))
        cursor.execute('DELETE FROM User WHERE user_id = ?', (self.booking[0],))
        conn.commit()
        for record in self.records: 
            if record.record[0] == self.records[0]:
                for widget in record.winfo_children():
                    widget.destroy()
                self.records.remove(record)
                del record

class ContentFrame(ctk.CTkFrame):
    def __init__(self, parent, user, card):
        super().__init__(parent, width = 650, height = 550, border_color = "black", border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')
        self.user = user
        self.card = card
        ctk.CTkLabel(self, text = 'Welcome!', font = ('Impact', 140)).place(anchor = 'center', relx = 0.5, rely = 0.5)

#Account Edit
    def account_edit_page(self):
        self.clear_frame()
        self.password_entry = ctk.StringVar()
        self.confirm_password_entry = ctk.StringVar()
        heading_font = ctk.CTkFont(family = 'Impact', size = 75, underline = True)
        title_font = ctk.CTkFont(family = 'Impact', size = 40, underline = True)
        info_font = ctk.CTkFont(family = 'Impact', size = 40)
        ctk.CTkLabel(self, text = 'Profile', font = heading_font).place(anchor = 'center', relx = 0.5, rely = 0.15)
        ctk.CTkLabel(self, text = 'First Name:', font = title_font).place(anchor = 'center', relx = 0.2, rely = 0.33)
        ctk.CTkLabel(self, text = self.user.first_name, font = info_font).place(anchor = 'center', relx = 0.5, rely = 0.33)
        if self.user.user_id[0] == 'A':
            ctk.CTkLabel(self, text = 'User ID:', font = title_font).place(anchor = 'center', relx = 0.2, rely = 0.48)
            ctk.CTkLabel(self, text = self.user.user_id, font = info_font).place(anchor = 'center', relx = 0.5, rely = 0.48)
            ctk.CTkLabel(self, text = 'Card ID:', font = title_font).place(anchor = 'center', relx = 0.2, rely = 0.63)    
            ctk.CTkLabel(self, text = self.card.card_id, font = info_font).place(anchor = 'center', relx = 0.5, rely = 0.63)           
        elif self.user.user_id[0] == 'T' or self.user.user_id[0] == 'S':
            ctk.CTkLabel(self, text = 'Last Name:', font = title_font).place(anchor = 'center', relx = 0.2, rely = 0.48)
            ctk.CTkLabel(self, text = self.user.last_name, font = info_font).place(anchor = 'center', relx = 0.5, rely = 0.48)
            ctk.CTkLabel(self, text = 'User ID:', font = title_font).place(anchor = 'center', relx = 0.2, rely = 0.78)
            ctk.CTkLabel(self, text = self.user.user_id, font = info_font).place(anchor = 'center', relx = 0.5, rely = 0.78)
            ctk.CTkLabel(self, text = 'Card ID:', font = title_font).place(anchor = 'center', relx = 0.2, rely = 0.93)    
            ctk.CTkLabel(self, text = self.card.card_id, font = info_font).place(anchor = 'center', relx = 0.5, rely = 0.93)      
            if self.user.user_id[0] == 'T':
                facility_name = cursor.execute('SELECT facility_name FROM Facility WHERE facility_id = ?', (self.user.facility_id,)).fetchall()
                ctk.CTkLabel(self, text = 'Facility:', font = title_font).place(anchor = 'center', relx = 0.2, rely = 0.63)
                ctk.CTkLabel(self, text = facility_name, font = info_font).place(anchor = 'center', relx = 0.5, rely = 0.63)
            else:
                ctk.CTkLabel(self, text = 'Class:', font = title_font).place(anchor = 'center', relx = 0.2, rely = 0.63)
                ctk.CTkLabel(self, text = self.user.grade, font = info_font).place(anchor = 'center', relx = 0.5, rely = 0.63)
        ctk.CTkLabel(self, text = 'New Password', font = ('Impact', 20)).place(anchor = 'center', relx = 0.8, rely = 0.38)
        ctk.CTkEntry(self, textvariable = self.password_entry, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.8, rely = 0.43)
        ctk.CTkLabel(self, text = 'Confirm Password', font = ('Impact', 20)).place(anchor = 'center', relx = 0.8, rely = 0.58)
        ctk.CTkEntry(self, textvariable = self.confirm_password_entry, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.8, rely = 0.63)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', text = 'Update', font = ('Impact', 20), command = self.account_edit_func).place(anchor = 'center', relx = 0.8, rely = 0.78)        

    def account_edit_func(self):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if self.password_entry.get() == '' or self.confirm_password_entry.get() == '':
            messagebox.showerror("Register Failed", "All fields must be filled out.")
        elif self.password_entry.get() != self.confirm_password_entry.get():
            messagebox.showerror("Register Failed", "Please make sure the passwords are the same.")
        elif not re.match(pattern, self.password_entry.get()):
            messagebox.showerror("Register Failed", "Password is not strong enough. Please include: 8 Characters minimum, A capital letter, A small letter, A number, A symbol.")
        elif re.match(pattern, self.password_entry.get()):
            hashed_password, salt = self.password_hash()
            cursor.execute('''UPDATE User 
                            SET hashed_password = ?, salt = ?
                            WHERE user_id = ?;''', 
                            (hashed_password, salt, self.user.user_id))
            messagebox.showinfo('Password Successfully Set', 'Please login with the new password.')
            conn.commit()
            self.password_entry.set('')
            self.confirm_password_entry.set('')
    
    def password_hash(self):
        salt = secrets.token_bytes(16)
        salted_password = self.password_entry.get().encode('utf-8') + salt
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        return hashed_password, salt

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
        self.other_button = ctk.CTkSwitch(self, text = 'Other', command = self.other, variable = self.other_bool, progress_color = theme_color, button_color = 'black')
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
        self.day.set('')
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

#Approvals
    def approvals(self):
        self.clear_frame()
        if self.user.user_id[0] == 'A' or self.user.user_id[0] == 'T':
            if self.user.user_id[0] == 'A':
                bookings = cursor.execute('''SELECT Booking.booking_number, Facility.facility_name, Timeslot.start_time, Timeslot.end_time, Timeslot.day, Booking.booking_date, Booking.approved, Booking.timeslot_id, User.first_name, User.last_name, User.class_grade, User.user_id
                                            FROM Facility, Timeslot, Booking, User
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND Booking.approved IS NULL
                                            AND Booking.timeslot_id = Timeslot.timeslot_id
                                            AND User.user_id = Booking.user_id;''').fetchall()
            elif self.user.user_id[0] == 'T':
                bookings = cursor.execute('''SELECT Booking.booking_number, Facility.facility_name, Timeslot.start_time, Timeslot.end_time, Timeslot.day, Booking.booking_date, Booking.approved, Booking.timeslot_id, User.first_name, User.last_name, User.class_grade, User.user_id
                                            FROM Facility, Timeslot, Booking, User
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND Booking.approved IS NULL
                                            AND Booking.facility_id = ?
                                            AND Booking.timeslot_id = Timeslot.timeslot_id
                                            AND User.user_id = Booking.user_id;''', (self.user.facility,)).fetchall()
            if bookings != []:
                incoming_approval_object_frame = ctk.CTkScrollableFrame(self, width = 620, height = 342, corner_radius = 0, border_color = 'black', border_width = 2) #fg_color = '#F0F0F0')
                incoming_approval_object_frame.place(anchor = 'n', relx = 0.5, rely = 0.36)
                incoming_approval_objects = []
                for booking in bookings:
                    approval_object = Incoming_Approval_Segment(incoming_approval_object_frame, incoming_approval_objects, booking, self.card)
                    incoming_approval_objects.append(approval_object)
                title_font = ctk.CTkFont(family = 'Impact', size = 18, underline = True)
                ctk.CTkLabel(self, text = 'Incoming Approvals', font = ('Impact', 90)).place(anchor = 'center', relx = 0.5, rely = 0.15)
                ctk.CTkLabel(self, text = 'Facility', font = title_font).place(anchor = 'center', relx = 0.085, rely = 0.33)
                ctk.CTkLabel(self, text = 'Start Time', font = title_font).place(anchor = 'center', relx = 0.24, rely = 0.33)
                ctk.CTkLabel(self, text = 'End Time', font = title_font).place(anchor = 'center', relx = 0.39, rely = 0.33)
                ctk.CTkLabel(self, text = 'Day', font = title_font).place(anchor = 'center', relx = 0.545, rely = 0.33)
                ctk.CTkLabel(self, text = 'Date', font = title_font).place(anchor = 'center', relx = 0.695, rely = 0.33)
                ctk.CTkLabel(self, text = 'Status', font = title_font).place(anchor = 'center', relx = 0.855, rely = 0.33)
            else:
                ctk.CTkLabel(self, text = 'There are no incoming requests', font = ('Impact', 45)).place(anchor = 'center', relx = 0.5, rely = 0.5)   
        else:
            bookings = cursor.execute('''SELECT Booking.booking_number, Facility.facility_name, Timeslot.start_time, Timeslot.end_time, Timeslot.day, Booking.booking_date, Booking.approved, Booking.timeslot_id 
                                        FROM Facility, Timeslot, Booking 
                                        WHERE Facility.facility_id = Booking.facility_id
                                            AND Timeslot.timeslot_id = Booking.timeslot_id
                                            AND Booking.user_id = ?;''', (self.user.user_id,)).fetchall()
            if bookings != []:
                outgoing_approval_object_frame = ctk.CTkScrollableFrame(self, width = 620, height = 342, corner_radius = 0, border_color = 'black', border_width = 2) #fg_color = '#F0F0F0')
                outgoing_approval_object_frame.place(anchor = 'n', relx = 0.5, rely = 0.36)
                outgoing_approval_objects = []
                for booking in bookings:
                    if booking[6] == None: status = 'Pending'
                    elif booking[6] == 1: status = 'Approved'
                    else: status = 'Declined'
                    approval_object = Outgoing_Approval_Segment(outgoing_approval_object_frame, booking, status, outgoing_approval_objects)
                    outgoing_approval_objects.append(approval_object)
                title_font = ctk.CTkFont(family = 'Impact', size = 18, underline = True)
                ctk.CTkLabel(self, text = 'Sent Approvals', font = ('Impact', 90)).place(anchor = 'center', relx = 0.5, rely = 0.15)
                ctk.CTkLabel(self, text = 'Facility', font = title_font).place(anchor = 'center', relx = 0.085, rely = 0.33)
                ctk.CTkLabel(self, text = 'Start Time', font = title_font).place(anchor = 'center', relx = 0.24, rely = 0.33)
                ctk.CTkLabel(self, text = 'End Time', font = title_font).place(anchor = 'center', relx = 0.39, rely = 0.33)
                ctk.CTkLabel(self, text = 'Day', font = title_font).place(anchor = 'center', relx = 0.545, rely = 0.33)
                ctk.CTkLabel(self, text = 'Date', font = title_font).place(anchor = 'center', relx = 0.695, rely = 0.33)
                ctk.CTkLabel(self, text = 'Status', font = title_font).place(anchor = 'center', relx = 0.855, rely = 0.33)
            else:
                ctk.CTkLabel(self, text = 'You have no requests sent', font = ('Impact', 50)).place(anchor = 'center', relx = 0.5, rely = 0.5)

#Schedule Viewer
    def schedule_viewer(self):
        self.clear_frame()
        if self.user.user_id[0] == 'A':
            bookings = cursor.execute('''SELECT Booking.booking_number, Facility.facility_name, Timeslot.start_time, Timeslot.end_time, Timeslot.day, Booking.booking_date, Booking.approved, Booking.timeslot_id, User.first_name, User.last_name, User.class_grade, User.user_id
                                        FROM Facility, Timeslot, Booking, User
                                        WHERE Booking.facility_id = Facility.facility_id
                                        AND Booking.approved = TRUE
                                        AND Booking.timeslot_id = Timeslot.timeslot_id
                                        AND User.user_id = Booking.user_id;''').fetchall()
        elif self.user.user_id[0] == 'T':
            bookings = cursor.execute('''SELECT Booking.booking_number, Facility.facility_name, Timeslot.start_time, Timeslot.end_time, Timeslot.day, Booking.booking_date, Booking.approved, Booking.timeslot_id, User.first_name, User.last_name, User.class_grade, User.user_id
                                        FROM Facility, Timeslot, Booking, User
                                        WHERE Booking.facility_id = Facility.facility_id
                                        AND Booking.approved = TRUE
                                        AND Booking.timeslot_id = Timeslot.timeslot_id
                                        AND User.user_id = Booking.user_id
                                        AND Facility.facility_id = ?;''', (self.user.facility_id,)).fetchall()
        if bookings != []:
            booking_objects = []
            bookings_frame = ctk.CTkScrollableFrame(self, width = 620, height = 342, corner_radius = 0, border_color = 'black', border_width = 2) #fg_color = '#F0F0F0')
            bookings_frame.place(anchor = 'n', relx = 0.5, rely = 0.36)
            for booking in bookings:
                approval_object = Scheduled_Booking_Segment(bookings_frame, booking_objects, booking, self.card, self.user)
                booking_objects.append(approval_object)
            title_font = ctk.CTkFont(family = 'Impact', size = 18, underline = True)
            ctk.CTkLabel(self, text = 'Scheduled Bookings', font = ('Impact', 75)).place(anchor = 'center', relx = 0.5, rely = 0.15)
            ctk.CTkLabel(self, text = 'User ID', font = title_font).place(anchor = 'center', relx = 0.085, rely = 0.33)
            ctk.CTkLabel(self, text = 'Facility', font = title_font).place(anchor = 'center', relx = 0.24, rely = 0.33)
            ctk.CTkLabel(self, text = 'Start Time', font = title_font).place(anchor = 'center', relx = 0.39, rely = 0.33)
            ctk.CTkLabel(self, text = 'End Time', font = title_font).place(anchor = 'center', relx = 0.545, rely = 0.33)
            ctk.CTkLabel(self, text = 'Day', font = title_font).place(anchor = 'center', relx = 0.695, rely = 0.33)
            ctk.CTkLabel(self, text = 'Date', font = title_font).place(anchor = 'center', relx = 0.855, rely = 0.33)
        else:
            ctk.CTkLabel(self, text = 'Empty Schedule', font = ('Impact', 50)).place(anchor = 'center', relx = 0.5, rely = 0.5)

#Record Viewer   
    def all_records_page(self):
        self.selection_occupation = ctk.StringVar()
        self.selection_facility = ctk.StringVar()
        self.all_records()

    def all_records(self):
        self.clear_frame()
        self.occupations = ('All', 'Teachers', 'Students')
        self.facilities = ('All', 'Football', 'Sixth Form Room', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')
        heading_font = ctk.CTkFont(family = 'Impact', size = 90, underline = True)
        ctk.CTkLabel(self, text = 'Records', font = heading_font).place(anchor = 'center', relx = 0.34, rely = 0.18)
        ctk.CTkComboBox(self, variable = self.selection_occupation, values = self.occupations, state = 'readonly', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15)).place(anchor = 'center', relx = 0.8, rely = 0.08)
        self.facility_combobox = ctk.CTkComboBox(self, variable = self.selection_facility, values = self.facilities, state = 'readonly', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15))
        self.facility_combobox.place(anchor = 'center', relx = 0.8, rely = 0.18)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', text = 'Search', font = ('Impact', 20), command = self.all_records).place(anchor = 'center', relx = 0.8, rely = 0.28)
        if self.user.user_id[0] == 'A':
            if self.selection_occupation.get() == '':
                self.selection_occupation.set('All')
                self.selection_facility.set('All')
            if self.selection_occupation.get() == 'All':
                    self.facility_combobox.configure(state = 'disabled')    
                    teacher_records = cursor.execute('''SELECT User.user_id, facility_name, first_name, last_name, card_id
                                            FROM User, Card, Facility
                                            WHERE User.user_id = Card.user_id
                                            AND User.user_id <> 'A'
                                            AND Facility.facility_id = User.facility_id;''').fetchall()
                    student_records = cursor.execute('''SELECT User.user_id, class_grade, first_name, last_name, card_id
                                            FROM User, Card
                                            WHERE User.user_id = Card.user_id
                                            AND User.user_id <> 'A'
                                            AND User.facility_id IS NULL''').fetchall()
                    records = teacher_records + student_records
            elif self.selection_occupation.get() == 'Teachers':
                self.facility_combobox.configure(state = 'readonly')    
                if self.selection_facility.get() == 'All':
                    records = cursor.execute('''SELECT User.user_id, facility_name, first_name, last_name, card_id
                                            FROM User, Card, Facility
                                            WHERE User.user_id = Card.user_id
                                            AND User.user_id <> 'A'
                                            AND Facility.facility_id = User.facility_id;''').fetchall()
                else:
                    records = cursor.execute('''SELECT User.user_id, facility_name, first_name, last_name, card_id
                                            FROM User, Card, Facility
                                            WHERE User.user_id = Card.user_id
                                            AND User.user_id <> 'A'
                                            AND Facility.facility_id = User.facility_id
                                            AND Facility.facility_name = ?;''', (self.selection_facility.get(),)).fetchall()
            elif self.selection_occupation.get() == 'Students':
                self.facility_combobox.configure(state = 'disabled')    
                records = cursor.execute('''SELECT User.user_id, class_grade, first_name, last_name, card_id
                                            FROM User, Card
                                            WHERE User.user_id = Card.user_id
                                            AND User.user_id <> 'A'
                                            AND User.facility_id IS NULL''').fetchall()
        elif self.user.user_id[0] == 'T':
            records = cursor.execute('''SELECT User.user_id, class_grade, first_name, last_name, card_id
                                    FROM User, Card, Facility
                                    WHERE User.user_id = Card.user_id
                                    AND User.user_id <> 'A'
                                    AND User.facility_id IS NULL
                                    AND Facility.facility_id = ?;''', (self.user.facility_id,)).fetchall()
        if records != []:
            record_objects = []
            records_frame = ctk.CTkScrollableFrame(self, width = 620, height = 330, corner_radius = 0, border_color = 'black', border_width = 2)
            records_frame.place(anchor = 'n', relx = 0.5, rely = 0.382)
            for record in records:
                record_obj = Records(records_frame, self.user, record, record_objects)
                record_objects.append(record_obj)    
            title_font = ctk.CTkFont(family = 'Impact', size = 18, underline = True)
            ctk.CTkLabel(self, text = 'User ID', font = title_font).place(anchor = 'center', relx = 0.15, rely = 0.35)
            ctk.CTkLabel(self, text = 'Card ID', font = title_font).place(anchor = 'center', relx = 0.77, rely = 0.35)
            ctk.CTkLabel(self, text = 'Class/Facility', font = title_font).place(anchor = 'center', relx = 0.3, rely = 0.35)
            ctk.CTkLabel(self, text = 'First Name', font = title_font).place(anchor = 'center', relx = 0.465, rely = 0.35)
            ctk.CTkLabel(self, text = 'Last Name', font = title_font).place(anchor = 'center', relx = 0.61, rely = 0.35)
        else:
            ctk.CTkLabel(self, text = 'There are no records', font = ('Impact', 50)).place(anchor = 'center', relx = 0.5, rely = 0.5)

#Analytics
    def analytics_page(self):
        self.clear_frame()
        ctk.CTkButton(self, text = 'Bookings per facility', hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.bookings_per_facility_page).place(anchor = 'center', relx = 0.5, rely = 0.1)
        ctk.CTkButton(self, text = 'Booking trends over time', hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.booking_trends_over_time_page).place(anchor = 'center', relx = 0.5, rely = 0.2)

    def bookings_per_facility_page(self):
        self.clear_frame()
        self.options = ('All-Time', 'Day', 'Date')
        self.option = ctk.StringVar()
        self.option.set('All-Time')
        self.facilities = ('All', 'Football', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')
        self.facility = ctk.StringVar()
        self.facility.set('All')
        self.statuses = ('All', 'Approved', 'Pending', 'Declined')
        self.statuses_dict = {'Approved': 1, 'Pending': None, 'Declined': 0}
        self.status = ctk.StringVar()
        self.status.set('All')
        self.days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
        self.day = ctk.StringVar()
        ctk.CTkComboBox(self, variable = self.option, values = self.options, state = 'readonly', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15), command = self.options_choice_bookings_per_facility_page).place(anchor = 'center', relx = 0.5, rely = 0.1)
        ctk.CTkComboBox(self, variable = self.facility, values = self.facilities, state = 'readonly', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15)).place(anchor = 'center', relx = 0.5, rely = 0.2)
        ctk.CTkComboBox(self, variable = self.status, values = self.statuses, state = 'readonly', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15)).place(anchor = 'center', relx = 0.5, rely = 0.3)
        self.days_combobox = ctk.CTkComboBox(self, variable = self.day, values = self.days, state = 'disabled', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15))
        self.days_combobox.place(anchor = 'center', relx = 0.5, rely = 0.4)
        self.start_date_button = ctk.CTkButton(self, state = 'disabled', hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Select Start Date", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.get_start_date)
        self.start_date_button.place(anchor = 'center', relx = 0.5, rely = 0.5)
        self.end_date_button = ctk.CTkButton(self, state = 'disabled', hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Select End Date", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.get_end_date)
        self.end_date_button.place(anchor = 'center', relx = 0.5, rely = 0.6)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = 'Generate', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.bookings_per_facility_func).place(anchor = 'center', relx = 0.5, rely = 0.7)
    
    def options_choice_bookings_per_facility_page(self, event):
        if event == 'Day':
            self.days_combobox.configure(state = 'readonly')
            self.start_date_button.configure(state = 'disabled')
            self.end_date_button.configure(state = 'disabled')
        elif event == 'Date':
            self.days_combobox.configure(state = 'disabled')
            self.start_date_button.configure(state = 'normal')
            self.end_date_button.configure(state = 'normal')

    def get_start_date(self):
        calender = Querybox()
        self.start_date = calender.get_date(title = 'Calender', bootstyle = 'dark')
        self.start_date_button.configure(text = self.start_date)
    
    def get_end_date(self):
        calender = Querybox()
        self.end_date = calender.get_date(title = 'Calender', bootstyle = 'dark')
        self.end_date_button.configure(text = self.end_date)

    def bookings_per_facility_func(self):
        if self.option.get() == 'All-Time':
            if self.facility.get() == 'All':
                if self.status.get() == 'All':
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility
                                            WHERE Booking.facility_id = Facility.facility_id
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''').fetchall()
                    title = 'Total Booking Counts Per Facility'
                else:
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND Booking.approved = ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''', (self.statuses[self.status.get()],)).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.statuses_dict[self.status.get()]})'
            else:
                if self.status.get() == 'All':
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND Facility.facility_name = ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''', (self.facility.get(),)).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.facility.get()})'
                else:
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND Facility.facility_name = ?
                                            AND Booking.approved = ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''', 
                                            (self.facility.get(), self.statuses_dict[self.status.get()])).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.facility.get()})({self.status.get()})'
        elif self.option.get() == 'Day':
            if self.facility.get() == 'All':
                if self.status.get() == 'All':
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility, Timeslot
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND Booking.timeslot_id = Timeslot.timeslot_id
                                            AND Timeslot.day = ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''', (self.day.get(),)).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.day.get()})'
                else:
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility, Timeslot
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND Booking.timeslot_id = Timeslot.timeslot_id
                                            AND Timeslot.day = ?
                                            AND Booking.approved = ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''',
                                            (self.day.get(), self.statuses_dict[self.status.get()])).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.day.get()})({self.status.get()})'
            else:
                if self.status.get() == 'All':
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility, Timeslot
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND Booking.timeslot_id = Timeslot.timeslot_id
                                            AND Timeslot.day = ?
                                            AND Facility.facility_name = ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''', (self.day.get(), self.facility.get())).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.day.get()})({self.facility.get()})'
                else:
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility, Timeslot
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND Booking.timeslot_id = Timeslot.timeslot_id
                                            AND Timeslot.day = ?
                                            AND Facility.facility_name = ?
                                            AND Booking.approved = ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''', (self.day.get(), self.facility.get(), self.statuses_dict[self.status.get()])).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.day.get()})({self.facility.get()})({self.status.get()})'
        else:
            if self.facility.get() == 'All':
                if self.status.get() == 'All':
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND booking_date >= ?
                                            AND booking_date <= ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''', (self.start_date, self.end_date)).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.start_date}) to ({self.end_date})'
                else:
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND booking_date >= ?
                                            AND booking_date <= ?
                                            AND Booking.approved = ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''',
                                            (self.start_date, self.end_date, self.statuses_dict[self.status.get()])).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.start_date}) to ({self.end_date})({self.status.get()})'
            else:
                if self.status.get() == 'All':
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND booking_date >= ?
                                            AND booking_date <= ?
                                            AND Facility.facility_name = ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''', (self.start_date, self.end_date, self.facility.get())).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.start_date}) to ({self.end_date})({self.facility.get()})'
                else:
                    result = cursor.execute('''SELECT facility_name, COUNT(*) as booking_count
                                            FROM Booking, Facility
                                            WHERE Booking.facility_id = Facility.facility_id
                                            AND booking_date >= ?
                                            AND booking_date <= ?
                                            AND Facility.facility_name = ?
                                            AND Booking.approved = ?
                                            GROUP BY facility_name
                                            ORDER BY booking_count DESC''', (self.start_date, self.end_date, self.facility.get(), self.statuses_dict[self.status.get()])).fetchall()
                    title = f'Total Booking Counts Per Facility ({self.start_date}) to ({self.end_date})({self.facility.get()})({self.status.get()})'
        if result != []:
            facilities, counts = zip(*result)
            plt.figure(figsize = (10, 6), edgecolor = 'black')
            plt.bar(facilities, counts, color = theme_color, edgecolor = 'black')
            plt.title(title)
            plt.xlabel('Facility')
            plt.ylabel('Booking Count')
            plt.grid(axis='y')
            mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f'Value: {counts[sel.target.index]}'))
            plt.show()
        else:
            messagebox.showinfo('No Results', 'There are no bookings of this configuration.')

    def booking_trends_over_time_page(self):
        self.clear_frame()
        self.options = ('All-Time', 'Date')
        self.option = ctk.StringVar()
        self.option.set('All-Time')
        self.facilities = ('All', 'Football', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')
        self.facility = ctk.StringVar()
        self.facility.set('All')
        ctk.CTkComboBox(self, variable = self.option, values = self.options, state = 'readonly', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15), command = self.options_choice_booking_trends_over_time_page).place(anchor = 'center', relx = 0.5, rely = 0.1)
        ctk.CTkComboBox(self, variable = self.facility, values = self.facilities, state = 'readonly', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15)).place(anchor = 'center', relx = 0.5, rely = 0.2)
        self.start_date_button = ctk.CTkButton(self, state = 'disabled', hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Select Start Date", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.get_start_date)
        self.start_date_button.place(anchor = 'center', relx = 0.5, rely = 0.3)
        self.end_date_button = ctk.CTkButton(self, state = 'disabled', hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Select End Date", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.get_end_date)
        self.end_date_button.place(anchor = 'center', relx = 0.5, rely = 0.4)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = 'Generate', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.booking_trends_over_time_func).place(anchor = 'center', relx = 0.5, rely = 0.5)

    def options_choice_booking_trends_over_time_page(self, event):
            if event == 'All-Time':
                self.start_date_button.configure(state = 'disabled')
                self.end_date_button.configure(state = 'disabled')
            else:
                self.start_date_button.configure(state = 'normal')
                self.end_date_button.configure(state = 'normal')

    def booking_trends_over_time_func(self):
        if self.option.get() == 'All-Time':
            if self.facility.get() == 'All':
                result = cursor.execute('''SELECT booking_date, COUNT(*) as booking_count
                                        FROM Booking
                                        GROUP BY booking_date
                                        ORDER BY booking_date;''').fetchall()
            else:
                result = cursor.execute('''SELECT booking_date, COUNT(*) as booking_count
                                        FROM Booking, Facility
                                        WHERE Booking.facility_id = Facility.facility_id
                                        AND facility_name = ?
                                        GROUP BY booking_date
                                        ORDER BY booking_date;''', (self.facility.get(),)).fetchall()    
        else:
            if self.facility.get() == 'All':
                result = cursor.execute('''SELECT booking_date, COUNT(*) as booking_count
                                        FROM Booking
                                        WHERE booking_date >= ?
                                        AND booking_date <= ?
                                        GROUP BY booking_date
                                        ORDER BY booking_date;''', (self.start_date, self.end_date)).fetchall()   
            else:
                result = cursor.execute('''SELECT booking_date, COUNT(*) as booking_count
                                        FROM Booking
                                        WHERE Booking.facility_id = Facility.facility_id
                                        AND booking_date >= ?
                                        AND booking_date <= ?
                                        AND Facility.facility_name = ?
                                        GROUP BY booking_date
                                        ORDER BY booking_date;''', (self.start_date, self.end_date, self.facility.get())).fetchall()            
        if result != []:
            # Separate dates and counts
            dates, counts = zip(*result)

            # Convert date strings to datetime objects
            dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

            # Plot the data
            plt.figure(figsize=(10, 6))
            plt.plot_date(dates, counts, '-', color = theme_color)
            plt.title('Booking Trends Over Time')
            plt.xlabel('Date')
            plt.ylabel('Booking Count')

            # Formatting the x-axis to show dates nicely
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.gcf().autofmt_xdate()
            plt.show()
        else:
            messagebox.showinfo('No Results', 'There are no bookings of this configuration.')

    def popular_timings_page(self):
        self.clear_frame()
        self.options = ('All-Time', 'Day', 'Date')
        self.option = ctk.StringVar()
        self.option.set('All-Time')
        self.facilities = ('All', 'Football', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite')
        self.facility = ctk.StringVar()
        self.facility.set('All')
        self.days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
        self.day = ctk.StringVar()
        ctk.CTkComboBox(self, variable = self.option, values = self.options, state = 'readonly', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15), command = self.options_choice_bookings_per_facility_page).place(anchor = 'center', relx = 0.5, rely = 0.1)
        ctk.CTkComboBox(self, variable = self.facility, values = self.facilities, state = 'readonly', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15)).place(anchor = 'center', relx = 0.5, rely = 0.2)
        ctk.CTkComboBox(self, variable = self.status, values = self.statuses, state = 'readonly', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15)).place(anchor = 'center', relx = 0.5, rely = 0.3)
        self.days_combobox = ctk.CTkComboBox(self, variable = self.day, values = self.days, state = 'disabled', border_color = 'black', button_color = 'black', dropdown_font = ('Impact', 15))
        self.days_combobox.place(anchor = 'center', relx = 0.5, rely = 0.4)
        self.start_date_button = ctk.CTkButton(self, state = 'disabled', hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Select Start Date", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.get_start_date)
        self.start_date_button.place(anchor = 'center', relx = 0.5, rely = 0.5)
        self.end_date_button = ctk.CTkButton(self, state = 'disabled', hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = "Select End Date", text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.get_end_date)
        self.end_date_button.place(anchor = 'center', relx = 0.5, rely = 0.6)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = 'Generate', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = self.bookings_per_facility_func).place(anchor = 'center', relx = 0.5, rely = 0.7)
        
#Reset Content Frame
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

class SideBar(ctk.CTkFrame):
    def __init__(self, parent, login, page):
        super().__init__(parent, width = 200, height = 600, border_color = "black", border_width = 2, corner_radius = 0, fg_color = '#F0F0F0')
        profile_icon = ctk.CTkImage(light_image = Image.open("Images/profile.png"), size = (70,70))
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, text = '', image = profile_icon, width = 100, height = 100, text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.account_edit_page).place(anchor = 'center', relx = 0.5, rely = 0.15)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Tap In', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.card_tap_in_page).place(anchor = 'center', relx = 0.5, rely = 0.3)
        ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Analytics', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.analytics_page).place(anchor = 'center', relx = 0.5, rely = 0.6)
        if login.user.user_id[0] == 'A' or login.user.user_id[0] == 'T':
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Schedule Viewer', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.schedule_viewer).place(anchor = 'center', relx = 0.5, rely = 0.4)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Approvals', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.approvals).place(anchor = 'center', relx = 0.5, rely = 0.5)
            if login.user.user_id[0] == 'A':
                ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'All Records', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.all_records_page).place(anchor = 'center', relx = 0.5, rely = 0.7)
            else:
                ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Facility Records', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.all_records_page).place(anchor = 'center', relx = 0.5, rely = 0.7)
        else:
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Facility Support', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.facility_support).place(anchor = 'center', relx = 0.5, rely = 0.4)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'View Sent Approvals', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.approvals).place(anchor = 'center', relx = 0.5, rely = 0.5)
            ctk.CTkButton(self, hover_color = '#d4d4d4', border_color = 'black', border_width = 2, width = 180, text = 'Approval Request', text_color = 'black', fg_color = 'white', font = ('Impact', 20), command = page.approval_request).place(anchor = 'center', relx = 0.5, rely = 0.7)
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
        ctk.CTkLabel(login_frame, text = 'Set New Password', font = ('Impact', 60)).place(anchor = 'center', relx = 0.5, rely = 0.17)
        ctk.CTkLabel(login_frame, text = 'User ID', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.3)
        ctk.CTkEntry(login_frame, textvariable = self.id_entry, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.5, rely = 0.35)
        ctk.CTkLabel(login_frame, text = 'Password', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.45)
        ctk.CTkEntry(login_frame, textvariable = self.password_entry, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.5, rely = 0.5)
        ctk.CTkLabel(login_frame, text = 'Confirm Password', font = ('Impact', 20)).place(anchor = 'center', relx = 0.5, rely = 0.6)
        ctk.CTkEntry(login_frame, textvariable = self.confirm_password_entry, width = 190, border_color = 'black', border_width = 2, corner_radius = 0).place(anchor = 'center', relx = 0.5, rely = 0.65)

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
