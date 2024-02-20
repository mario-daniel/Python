from datetime import datetime
import sqlite3
import customtkinter as ctk
from tkinter import messagebox

conn = sqlite3.connect("rfid")
cursor = conn.cursor()

window = ctk.CTk()
window.title('RFID System')
window.geometry('600x600')
ctk.set_appearance_mode('light')

combobox_variable = ctk.StringVar()
ctk.CTkComboBox(window, values = ('Football', 'Basketball', 'Cricket', 'Multi-Purpose Hall', 'Fitness Suite'), variable = combobox_variable)
ctk.CTkButton(window, text = 'Tap In', command = lambda: print())

def card_tap_in():
    if combobox_variable.get() == 'Football':
        current_date_time = datetime.now()
        current_time = current_date_time.strftime('%H:%M:%S')
        current_date = current_date_time.strftime('%d:%m:%Y')
        booking_date_info = cursor.execute('''SELECT start_time, end_time, booking_date, card_id 
                                        FROM User, Booking, Timeslot
                                        WHERE User.user_id = Booking.user_id
                                        AND User.user_id = ?
                                        AND Timeslot.timeslot_id = Booking.timeslot_id
                                        AND Timeslot.status = 1''')

window.mainloop()