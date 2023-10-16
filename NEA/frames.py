import tkinter as tk
from tkinter import ttk
from login import main_frame

window = tk.Tk()
window.geometry('400x200')
window.title('Student RFID')

window.rowconfigure(0, weight = 1)
window.columnconfigure(0, weight = 1)

login_menu = main_frame
register_menu = ttk.Frame(window)

Frames = [login_menu, register_menu]

for frame in Frames:
    frame.grid(row = 0, column = 0, sticky = 'nsew')